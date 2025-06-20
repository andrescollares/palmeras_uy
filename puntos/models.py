from django.contrib.gis.db import models


# Create your models here.
class Palmera(models.Model):
    codigo = models.CharField(max_length=32, unique=True, verbose_name="Código")
    coords = models.PointField(geography=True, verbose_name="Coordenadas", srid=4326)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    zona = models.CharField(max_length=100, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)
    dudas = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_extraccion = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = "Palmera"
        verbose_name_plural = "Palmeras"
        ordering = ["created_at"]


class Tratamiento(models.Model):
    palmera = models.ForeignKey(
        Palmera, on_delete=models.CASCADE, related_name="tratamientos"
    )

    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.palmera} - {self.id}"


class Monitoreo(models.Model):
    palmera = models.ForeignKey(
        "Palmera", on_delete=models.CASCADE, related_name="monitoreos"
    )

    fecha = models.DateTimeField(blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.palmera} - {self.id}"

    class Meta:
        ordering = ["fecha"]
