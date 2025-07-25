from django.contrib import admin
from .models import Reservation
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from django.db import models


@admin.register(Reservation)
class ReservationAdmin(ModelAdmin):
    autocomplete_fields = ['user', 'package']
    list_display = ('user', 'package', 'total_price', 'status', 'payment_method', 'payment_status', 'date','created_at','meeting_status')
    list_filter = ('status', 'payment_method', 'payment_status','date','created_at','meeting_status')
    search_fields = ('user__email', 'package__booking_type__name','meeting_status')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs

        if request.user.is_staff and request.user.has_perm('reservations.view_reservation'):
            return qs.filter(user=request.user)
        return qs.none()