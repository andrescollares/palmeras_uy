from django import forms
from django.contrib.gis import admin
from django.shortcuts import render
from django.urls import path

from puntos.csv_import import handle_csv_upload
from .models import Monitoreo, Palmera, Tratamiento


class TratamientoInline(admin.TabularInline):
    model = Tratamiento
    extra = 0
    verbose_name = "Tratamiento"
    verbose_name_plural = "Tratamientos"
    ordering = ["fecha"]


class MonitoreoInline(admin.TabularInline):
    model = Monitoreo
    extra = 0
    verbose_name = "Monitoreo"
    verbose_name_plural = "Monitoreos"
    ordering = ["fecha"]


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Archivo CSV",
        help_text="Sube un archivo CSV con los datos de las palmeras.",
    )


@admin.register(Palmera)
class PalmeraAdmin(admin.GISModelAdmin):
    change_list_template = "admin/palmera_changelist.html"
    inlines = [TratamientoInline, MonitoreoInline]

    list_display = (
        "codigo",
        "zona",
        "especie",
        "num_tratamientos",
        "num_monitoreos",
        "created_at",
        "updated_at",
    )

    def num_tratamientos(self, obj):
        return obj.tratamientos.count()

    num_tratamientos.short_description = "Tratamientos"

    def num_monitoreos(self, obj):
        return obj.monitoreos.count()

    num_monitoreos.short_description = "Monitoreos"

    gis_widget_kwargs = {
        "attrs": {
            "default_lon": -56.1645,  # Approximate center of Montevideo
            "default_lat": -34.9011,
            "default_zoom": 11,  # Zoomed out enough to see the whole city
        }
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload_csv/",
                self.admin_site.admin_view(self.upload_csv),
                name="upload_palmera_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                return handle_csv_upload(request, form)
        else:
            form = CSVUploadForm()
        return render(
            request,
            "admin/csv_form.html",
            {"form": form},
        )
