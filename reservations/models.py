from django.db import models
from book.models import Booking
from users.models import User
# from features.models import Feature

STATUS_CHOICES = [
    ('pending', 'قيد الانتظار'),
    ('confirmed', 'مؤكد'),
    ('cancelled', 'ملغي'),
]
PAYMENT_METHOD_CHOICES = [
    ('cash', 'نقدي'),
    ('card', 'بطاقة'),
]
PAYMENT_STATUS_CHOICES = [
    ('pending', 'قيد الانتظار'),
    ('paid', 'مدفوع'),
    ('failed', 'فشل'),
    ('waiting_for_refund', 'قيد الانتظار للاسترجاع'),
    ('refunded', 'مسترجع'),
    ('cancelled', 'ملغي')
]
MEETING_STATUS_CHOICES = [
    ('pending', 'قيد الانتظار'),
    ('confirmed', 'مؤكد'),
    ('cancelled', 'ملغي'),
]

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reservations')
    package = models.ForeignKey(Booking, on_delete=models.CASCADE,related_name='reservations')
    # additional_features = models.ManyToManyField(Feature, blank=True)
    total_price = models.FloatField()
    date = models.DateField()
    meeting_status = models.CharField(max_length=20, choices=MEETING_STATUS_CHOICES, default='pending')
    # time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.user.phone_number} - {self.package.booking_type.display_name}"
    
    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['-created_at']
        # unique_together = ['package']
    
    def get_package_name(self):
        return self.package.booking_type.display_name
    
    def get_package_price(self):
        return self.package.total_price
    
    