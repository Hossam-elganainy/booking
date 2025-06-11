from rest_framework import serializers
from .models import BookingType, Booking

class BookingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingType
        fields = ['id', 'name', 'display_name', 'field_schema']

class BookingSerializer(serializers.ModelSerializer):
    booking_type_name = serializers.CharField(source='booking_type.display_name', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['reference_number', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)