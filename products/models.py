from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.FloatField()
    stock = models.IntegerField()
