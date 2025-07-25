from django.shortcuts import render
from rest_framework import generics
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework import permissions
# from core.utils import custom_exception_handler


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    # custom exception handler
    # def handle_exception(self, exc):
    #     return custom_exception_handler(exc, self.request)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationRetrieveView(generics.RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = Reservation.objects.get(id=kwargs['pk'])
        user = request.user
        if instance.user != user:
            return Response({"error": "You are not allowed to cancel this reservation"}, status=status.HTTP_403_FORBIDDEN)
        if instance.status == 'cancelled':
            return Response({"error": "This reservation is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        if instance.status == 'completed':
            return Response({"error": "Cannot cancel it. This reservation is already completed"}, status=status.HTTP_400_BAD_REQUEST)


        # Handle refund logic
        if instance.payment_status == 'paid':
            if instance.payment_method == 'cash':
                instance.payment_status = 'waiting_for_refund'
                instance.status = 'cancelled'
                instance.save()
                return Response({"message": "Reservation cancelled successfully. Waiting for refund."}, status=status.HTTP_200_OK)
            elif instance.payment_method == 'card':
                instance.payment_status = 'waiting_for_refund'
                instance.status = 'cancelled'
                instance.save()
                #TODO: refund the payment
                return Response({"message": "Reservation cancelled successfully. Waiting for refund."}, status=status.HTTP_200_OK)

        instance.status = 'cancelled'
        instance.payment_status = 'cancelled'
        instance.save()
        return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_200_OK)