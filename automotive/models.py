from django.db import models

# Create your models here.
class Car(models.Model):
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marca} : {self.modelo}" 