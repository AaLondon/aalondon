from django.db import models

# Create your models here.
class Postcode(models.Model):
    postcode = models.CharField(max_length=10,blank=False,null=False)
    longitude = models.FloatField(blank=False,null=False)
    latitude = models.FloatField(blank=False,null=False)

    def __str__(self):
        return self.postcode