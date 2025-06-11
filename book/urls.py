from django.urls import path
from .views import BookingTypeList, BookingList, BookingCreate

urlpatterns = [
    path('booking-types/', BookingTypeList.as_view(), name='booking-types'),
    path('bookings/', BookingList.as_view(), name='bookings'),
    path('bookings/create/', BookingCreate.as_view(), name='booking-create'),
]