from django.contrib import admin
from .models import TimeTag, TimeRecord, TimeReport, HealthMedicineTag, HealthRecord

admin.site.register(TimeRecord)
admin.site.register(TimeTag)
admin.site.register(TimeReport)
admin.site.register(HealthMedicineTag)
admin.site.register(HealthRecord)

class TimeRecordAdmin(admin.ModelAdmin):
    model = TimeRecord
    # showing what is hidden:
    readonly_fields = ['end', 'duration']

admin.site.unregister(TimeRecord)
admin.site.register(TimeRecord, TimeRecordAdmin)