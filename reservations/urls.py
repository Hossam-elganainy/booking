from django.urls import path
from .views import ReservationListCreateView, ReservationCancelView, ReservationRetrieveView

urlpatterns = [
    path('', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('<int:pk>/', ReservationRetrieveView.as_view(), name='reservation-id'),
    path('<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
]