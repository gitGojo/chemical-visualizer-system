from django.urls import path
from .views import UploadAPI, SummaryAPI, HistoryAPI, PDFReportAPI

urlpatterns = [
    path('upload/', UploadAPI.as_view(), name='upload_csv'),
    path('summary/', SummaryAPI.as_view(), name='get_summary'),
    path('history/', HistoryAPI.as_view(), name='get_history'),
    path('report_pdf/', PDFReportAPI.as_view(), name='get_pdf_report'),
]
