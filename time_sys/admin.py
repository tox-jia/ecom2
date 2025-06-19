from django.contrib import admin
from .models import TimeTag, TimeRecord, TimeReport

admin.site.register(TimeRecord)
admin.site.register(TimeTag)
admin.site.register(TimeReport)

class TimeRecordAdmin(admin.ModelAdmin):
    model = TimeRecord
    # showing what is hidden:
    readonly_fields = ['end', 'duration']

admin.site.unregister(TimeRecord)
admin.site.register(TimeRecord, TimeRecordAdmin)