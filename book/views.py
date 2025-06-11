#import generics 
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import BookingType, Booking
from .serializers import BookingTypeSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .schemas import HOTEL_SCHEMA, CAR_SCHEMA
from django.shortcuts import get_object_or_404

class BookingTypeList(ListAPIView):
    queryset = BookingType.objects.all()
    serializer_class = BookingTypeSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Create default booking types if they don't exist
        hotel_type, _ = BookingType.objects.get_or_create(
            name='hotel',
            defaults={
                'display_name': 'Hotel Booking',
                'field_schema': HOTEL_SCHEMA
            }
        )
        
        car_type, _ = BookingType.objects.get_or_create(
            name='car',
            defaults={
                'display_name': 'Car Rental',
                'field_schema': CAR_SCHEMA
            }
        )
        
        return BookingType.objects.all()



# class BookingTypeCreate(CreateAPIView):
#     queryset = BookingType.objects.all()
#     serializer_class = BookingTypeSerializer
    permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class BookingList(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreate(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the booking type and its schema
        booking_type_id = request.data.get('booking_type')
        booking_type = get_object_or_404(BookingType, id=booking_type_id)
        schema = booking_type.field_schema

        # Validate booking data against schema
        booking_data = request.data.get('booking_data', {})
        errors = {}

        for field_name, field_schema in schema.items():
            field_value = booking_data.get(field_name)
            
            # Check required fields
            if field_schema.get('required', False) and not field_value:
                errors[field_name] = f"{field_name} is required"
                continue

            # Validate field type
            if field_value:
                if field_schema['type'] == 'text' and not isinstance(field_value, str):
                    errors[field_name] = f"{field_name} must be text"
                elif field_schema['type'] == 'number':
                    try:
                        num_value = float(field_value)
                        if 'min' in field_schema and num_value < field_schema['min']:
                            errors[field_name] = f"{field_name} must be at least {field_schema['min']}"
                        if 'max' in field_schema and num_value > field_schema['max']:
                            errors[field_name] = f"{field_name} must be at most {field_schema['max']}"
                    except ValueError:
                        errors[field_name] = f"{field_name} must be a number"
                elif field_schema['type'] == 'choice' and field_value not in field_schema['choices']:
                    errors[field_name] = f"{field_name} must be one of {field_schema['choices']}"

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking with validated data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

