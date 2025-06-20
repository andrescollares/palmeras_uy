from django.contrib.gis import admin
from .models import Barrio


@admin.register(Barrio)
class BarrioAdmin(admin.GISModelAdmin):
    readonly_fields = ("nombre",)

    def save_model(self, request, obj, form, change):
        # Prevent updates to the geometry field
        original = self.model.objects.get(pk=obj.pk)
        obj.geom = original.geom
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # Disable adding new barrios through the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable deleting barrios through the admin interface
        return False
