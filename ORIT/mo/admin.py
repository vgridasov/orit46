from django.contrib import admin
from .models import MOModel, StaffModel


class MOModelAdmin(admin.ModelAdmin):
    list_display = (
        'sn',
        'name',
        'mo_type',
        'is_active',
        'aro_available',
        'pso_n_available',
        'pso_c_available',
        'ho_available',
    )
    list_display_links = ('sn', 'name',)



admin.site.register(MOModel, MOModelAdmin)


class StaffModelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'fio',
        'user',
        'is_fired',
    )


admin.site.register(StaffModel, StaffModelAdmin)
