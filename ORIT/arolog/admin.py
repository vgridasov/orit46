from django.contrib import admin
from .models import AROLogModel


class AROLogModelAdmin(admin.ModelAdmin):
    list_display = (
        'mh_num',
        'age',
        'edit_datetime',
        'to_hosp_date',
        'to_unit_date',
        'diagnosis',
        'mind',
        'vent',
        's_dyn',
        'registrator',
    )
    list_display_links = ('mh_num',)


admin.site.register(AROLogModel, AROLogModelAdmin)
