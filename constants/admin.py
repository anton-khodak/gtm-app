from django.contrib import admin

from constants.models import City, Area, Speciality, Hospital, Position, Department
from users.admin import admin_site


admin_site.register(City)
admin_site.register(Area)
admin_site.register(Speciality)
admin_site.register(Hospital)
admin_site.register(Position)
admin_site.register(Department)
# admin_site.register(Category)
# admin_site.register(CuringForm)