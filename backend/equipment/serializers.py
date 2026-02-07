from rest_framework import serializers
from .models import Equipment, Dataset

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['dataset', 'name', 'type', 'flowrate', 'pressure', 'temperature', 'uploaded_at']

class DatasetSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    uploaded_at = serializers.DateTimeField()
    total_equipment = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    type_distribution = serializers.DictField()
