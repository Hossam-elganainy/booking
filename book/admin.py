from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BookingType, Booking

@admin.register(BookingType)
class BookingTypeAdmin(ModelAdmin):
    list_display = ['display_name', 'name']

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ['reference_number', 'user', 'booking_type', 'status', 'created_at']
    list_filter = ['status', 'booking_type']
    search_fields = ['reference_number', 'user__email']