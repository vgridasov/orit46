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


class MOUnitModelAdmin(admin.ModelAdmin):
    list_display = (
        'sn',
        'mo',
        'name',
        'is_active',
    )
    list_display_links = ('sn', 'name',)


class StaffModelAdmin(admin.ModelAdmin):
    list_display = (
        'mo_unit',
        'fio',
        'user',
        'email',
        'is_active',
    )
    list_display_links = (
        'mo_unit',
        'fio',
    )


admin.site.register(MOModel, MOModelAdmin)
admin.site.register(MOUnitModel, MOUnitModelAdmin)
admin.site.register(StaffModel, StaffModelAdmin)
admin.site.register(BedSpaceNumberModel)

