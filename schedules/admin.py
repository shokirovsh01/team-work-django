from django.contrib import admin
from .models import WorkSchedule, TimeSlot, DayOff


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'get_weekday_display', 'start_time', 'end_time', 'slot_duration')
    list_filter = ('weekday',)
    search_fields = ('doctor__user__last_name',)

    def get_weekday_display(self, obj):
        return obj.get_weekday_display()
    get_weekday_display.short_description = 'День недели'


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('doctor__user__last_name',)


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'reason')
    search_fields = ('doctor__user__last_name',)






    