# Generated by Django 4.2.3 on 2023-09-05 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("out for shipping", "out for shipping"),
                    ("pending", "pending"),
                    ("completed", "completed"),
                ],
                default="Pending",
                max_length=150,
            ),
        ),
    ]
