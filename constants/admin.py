from constants.models import City, Area, Speciality, Hospital, Position, Department, Category, CuringForm
from users.admin import admin_site
from django.contrib import admin


class SpecialityAdmin(admin.ModelAdmin):
    model = Speciality
    ordering = ['name']
    search_fields = ['name']

class AreaAdmin(admin.ModelAdmin):
    model = Area
    ordering = ['name']
    search_fields = ['name']

class CityAdmin(admin.ModelAdmin):
    model = City
    ordering = ['name']
    search_fields = ['name']


admin_site.register(City, CityAdmin)
admin_site.register(Area, AreaAdmin)
admin_site.register(Speciality, SpecialityAdmin)
admin_site.register(Hospital)
admin_site.register(Position)
admin_site.register(Department)
admin_site.register(Category)
admin_site.register(CuringForm)