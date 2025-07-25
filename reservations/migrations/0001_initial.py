# Generated by Django 4.2.15 on 2025-07-25 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_price", models.FloatField()),
                ("date", models.DateField()),
                (
                    "meeting_status",
                    models.CharField(
                        choices=[
                            ("pending", "قيد الانتظار"),
                            ("confirmed", "مؤكد"),
                            ("cancelled", "ملغي"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "قيد الانتظار"),
                            ("confirmed", "مؤكد"),
                            ("cancelled", "ملغي"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("cash", "نقدي"), ("card", "بطاقة")],
                        default="cash",
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("pending", "قيد الانتظار"),
                            ("paid", "مدفوع"),
                            ("failed", "فشل"),
                            ("waiting_for_refund", "قيد الانتظار للاسترجاع"),
                            ("refunded", "مسترجع"),
                            ("cancelled", "ملغي"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="book.booking",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="users.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reservation",
                "verbose_name_plural": "Reservations",
                "ordering": ["-created_at"],
            },
        ),
    ]
