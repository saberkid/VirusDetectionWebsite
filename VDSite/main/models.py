from django.db import models

# Create your models here.
class Query_Result(models.Model):
    hash = models.CharField(max_length=50, primary_key=True)
    fortinet = models.CharField(max_length=50, default='None', null=True)
    positive = models.IntegerField(default=0, null=True)
    date = models.CharField(max_length=50, default='N/A', null=True)