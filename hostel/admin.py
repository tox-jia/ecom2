from django.contrib import admin
from .models import *


admin.site.register(Guest)
admin.site.register(Term)
admin.site.register(RoomState)
admin.site.register(Allergy)
admin.site.register(MonthlyJob)
admin.site.register(MonthlyJobRecord)
admin.site.register(Staff)
admin.site.register(StaffDayRecord)