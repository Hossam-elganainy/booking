from rest_framework import serializers
from .models import Reservation
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.db.models import Count
from book.models import Booking
from users.models import User


class ReservationSerializer(serializers.ModelSerializer):
    package_name = serializers.StringRelatedField(source='package', read_only=True)
    package_id = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all(), source='package', write_only=True)
    
    class Meta:
        model = Reservation
        exclude = ['user', 'package']
        read_only_fields = ['created_at', 'updated_at','status','total_price','payment_status','date','meeting_status']

        

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        validated_data['payment_status'] = 'pending'
        validated_data['meeting_status'] = 'pending'
        
        package = validated_data['package']
        total_price = package.total_price
            
        validated_data['total_price'] = total_price
        validated_data['date'] = timezone.now().date()

        reservation = super().create(validated_data)
        return reservation
    