from django.contrib import admin
from .models import Question, OnmkStat

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'sn',
        'title',
        'is_active',
        'calc',
    )
    list_display_links = ('sn', 'title',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(OnmkStat)
