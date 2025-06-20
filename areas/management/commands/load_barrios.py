from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping


class Command(BaseCommand):
    help = "Load barrio data from shapefile into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to load barrio data...")
        try:
            self.load_barrio_data()
            self.stdout.write("Barrio data loaded successfully.")
        except Exception as e:
            self.stdout.write(f"Error loading barrio data: {e}")

    def load_barrio_data(self):
        from areas.models import Barrio

        # Define the mapping for the shapefile fields to model fields
        barrio_mapping = {
            "nombre": "barrio",
            "geom": "MULTIPOLYGON",
        }

        # File is in shp and at project root /data/barrios_montevideo.shp
        lm = LayerMapping(
            Barrio,
            "data/barrios/barrios_montevideo.shp",
            barrio_mapping,
            transform=True,
            encoding="latin1",
        )
        lm.save(strict=True, verbose=True)
