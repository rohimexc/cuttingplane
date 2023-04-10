from django.db import models
class DataProses(models.Model):
    token=models.CharField(max_length=16, null=True)
    hasil=models.CharField(max_length=30, null=True)
    kendala=models.IntegerField(null=True)
    def __str__(self):
        return self.token


# Create your models here.
