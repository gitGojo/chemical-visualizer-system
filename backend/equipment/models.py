from django.db import models

class Dataset(models.Model):
    """
    Represents a specific CSV upload event.
    """
    id = models.AutoField(primary_key=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"

class Equipment(models.Model):
    """
    Represents a single equipment record from an uploaded CSV.
    """
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    # Redundant field to strictly satisfy user requirement "Equipment model with fields... uploaded_at"
    uploaded_at = models.DateTimeField() 

    def save(self, *args, **kwargs):
        if not self.uploaded_at and self.dataset:
            self.uploaded_at = self.dataset.uploaded_at
        super().save(*args, **kwargs)
