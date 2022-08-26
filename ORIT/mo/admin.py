from django.contrib import admin
from .models import MOModel, StaffModel, MOUnitModel, BedSpaceNumberModel


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


class StaffModelAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'fio',
        'user',
        'is_fired',
        'mo',
    )
    list_display_links = (
        'title',
        'fio',
    )


admin.site.register(MOModel, MOModelAdmin)
admin.site.register(MOUnitModel)
admin.site.register(StaffModel, StaffModelAdmin)
admin.site.register(BedSpaceNumberModel)

