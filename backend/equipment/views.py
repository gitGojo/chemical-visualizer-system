from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Avg, Count
from django.http import HttpResponse
import pandas as pd
from .models import Dataset, Equipment
from .serializers import DatasetSummarySerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class UploadAPI(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file)
            # Normalize columns: strip whitespace
            df.columns = df.columns.str.strip()
            
            required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                return Response(
                    {"error": f"Missing columns: {missing_cols}. Found: {list(df.columns)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create Dataset
            dataset = Dataset.objects.create(uploaded_at=timezone.now())

            # Parse and Save
            equipment_list = []
            for _, row in df.iterrows():
                equipment_list.append(Equipment(
                    dataset=dataset,
                    name=row['Equipment Name'],
                    type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature'],
                    uploaded_at=dataset.uploaded_at
                ))
            Equipment.objects.bulk_create(equipment_list)

            # History Management: Keep user's limit of 5
            all_datasets = Dataset.objects.all().order_by('-uploaded_at')
            if all_datasets.count() > 5:
                # Delete older datasets
                ids_to_keep = all_datasets.values_list('id', flat=True)[:5]
                Dataset.objects.exclude(id__in=ids_to_keep).delete()

            return Response({"message": "Upload successful", "dataset_id": dataset.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_summary_data(dataset):
    if not dataset:
        return None
    
    equipment = dataset.equipment.all()
    total_count = equipment.count()
    if total_count == 0:
        return None

    aggs = equipment.aggregate(
        avg_flow=Avg('flowrate'),
        avg_press=Avg('pressure'),
        avg_temp=Avg('temperature')
    )

    type_dist = list(equipment.values('type').annotate(count=Count('type')))
    # Convert query set to dict
    dist_dict = {item['type']: item['count'] for item in type_dist}

    return {
        'id': dataset.id,
        'uploaded_at': dataset.uploaded_at,
        'total_equipment': total_count,
        'avg_flowrate': aggs['avg_flow'],
        'avg_pressure': aggs['avg_press'],
        'avg_temperature': aggs['avg_temp'],
        'type_distribution': dist_dict
    }

class SummaryAPI(APIView):
    def get(self, request):
        # Get latest dataset
        latest = Dataset.objects.first() # Ordered by -uploaded_at
        if not latest:
            return Response({"message": "No data available"}, status=200)
        
        data = get_summary_data(latest)
        serializer = DatasetSummarySerializer(data)
        return Response(serializer.data)

class HistoryAPI(APIView):
    def get(self, request):
        datasets = Dataset.objects.all() # Ordered by -uploaded_at
        history = []
        for ds in datasets:
            data = get_summary_data(ds)
            if data:
                history.append(data)
        
        serializer = DatasetSummarySerializer(history, many=True)
        return Response(serializer.data)

class PDFReportAPI(APIView):
    def get(self, request):
        latest = Dataset.objects.first()
        if not latest:
            return Response({"error": "No data available"}, status=404)
        
        data = get_summary_data(latest)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Chemical Equipment Summary Report")
        
        p.setFont("Helvetica", 12)
        y = 720
        p.drawString(100, y, f"Dataset ID: {data['id']}")
        y -= 20
        p.drawString(100, y, f"Uploaded At: {data['uploaded_at']}")
        y -= 40
        
        p.drawString(100, y, f"Total Equipment: {data['total_equipment']}")
        y -= 20
        p.drawString(100, y, f"Average Flowrate: {data['avg_flowrate']:.2f}")
        y -= 20
        p.drawString(100, y, f"Average Pressure: {data['avg_pressure']:.2f}")
        y -= 20
        p.drawString(100, y, f"Average Temperature: {data['avg_temperature']:.2f}")
        y -= 40

        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Type Distribution:")
        y -= 25
        p.setFont("Helvetica", 12)
        for dtype, count in data['type_distribution'].items():
            p.drawString(120, y, f"- {dtype}: {count}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
