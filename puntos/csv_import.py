import csv
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.gis.geos import GEOSGeometry
from .models import Palmera, Tratamiento, Monitoreo

TRATAMIENTO_FIELDS = [
    ("TRATAMIENTO MAYO 2023", "2023-05-01"),
    ("TRATAMIENTO OCTUBRE 2023", "2023-10-01"),
    ("TRATAMIENTO ENERO 2024", "2024-01-01"),
    ("TRATAMIENTO MAYO 2024", "2024-05-01"),
    ("TRATAMIENTO JULIO 2024", "2024-07-01"),
    ("TRATAMIENTO SEPTIEMBRE 2024", "2024-09-01"),
    ("TRATAMIENTO OCTUBRE 2024", "2024-10-01"),
    ("TRATAMIENTO NOVIEMBRE 2024", "2024-11-01"),
    ("TRATAMIENTO DICIEMBRE 2024", "2024-12-01"),
    ("TRATAMIENTO ENERO 2025", "2025-01-01"),
    ("TRATAMIENTO FEBRERO 2025", "2025-02-01"),
]

MONITOREO_FIELDS = [
    ("Fecha M1", "Síntomas M1"),
    ("Fecha M2", "Síntomas M2"),
    ("Fecha M3", "Síntomas M3"),
]


def parse_datetime(value):
    try:
        return datetime.datetime.strptime(value.strip(), "%d/%m/%y %H:%M")
    except:
        return None


def parse_float(value):
    try:
        return float(value.replace(",", ".")) if value else None
    except:
        return None


def handle_csv_upload(request, form):
    file = request.FILES["csv_file"]
    lines = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(lines)

    count = 0
    for row in reader:
        try:
            palmera, created = Palmera.objects.update_or_create(
                coords=GEOSGeometry(row["WKT"]),
                codigo=row["ID"],
                zona=row["ZONA"],
                dudas=row["DUDAS"],
                especie=row["Especie de palmera"],
                observaciones=row["OBSERVACIONES"],
                fecha_extraccion=parse_datetime(row["FECHA EXTRACCIÓN"]),
            )
            if not created:
                palmera.monitoreos.all().delete()

            for f_fecha, f_sintomas in MONITOREO_FIELDS:
                fecha = parse_datetime(row[f_fecha])
                sintomas = row[f_sintomas]
                if fecha or sintomas:
                    Monitoreo.objects.create(
                        palmera=palmera, fecha=fecha, sintomas=sintomas
                    )

            for col_name, date_str in TRATAMIENTO_FIELDS:
                desc = row.get(col_name)
                if desc:
                    fecha = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    Tratamiento.objects.update_or_create(
                        palmera=palmera,
                        fecha=fecha,
                        defaults={"descripcion": desc.strip()},
                    )

            count += 1

        except Exception as e:
            messages.error(request, f"Error on row {count + 1}: {e}")

    messages.success(request, f"{count} palmeras imported.")
    return redirect("..")
