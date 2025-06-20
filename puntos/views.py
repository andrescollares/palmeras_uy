from django.http import HttpResponse
from django.shortcuts import render
from django.core.serializers import serialize
from .models import Palmera


def palmeras_geojson(request):
    geojson = serialize(
        "geojson",
        Palmera.objects.all(),
        geometry_field="coords",
        fields=["codigo", "zona", "especie"],
    )
    return HttpResponse(geojson, content_type="application/json")


def palmeras_map(request):
    return render(request, "palmeras/map.html")
