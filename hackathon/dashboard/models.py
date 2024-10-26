from django.db import models

# Create your models here.


class SavePoint(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    

class DangerArea(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    

class DangerPoints(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    danger_area = models.ForeignKey(DangerArea, on_delete=models.CASCADE)

    def __str__(self):
        return self.danger_area.name