from django.contrib.gis.db import models


class Barrio(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    geom = models.MultiPolygonField(geography=True, verbose_name="Geometría", srid=4326)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"
        ordering = ["nombre"]
