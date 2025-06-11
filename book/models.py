from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    field_schema = models.JSONField(default=dict)
    
    def __str__(self):
        return self.display_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    reference_number = models.CharField(max_length=20, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    booking_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            import random
            self.reference_number = f"{self.booking_type.name.upper()[:3]}-{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.reference_number