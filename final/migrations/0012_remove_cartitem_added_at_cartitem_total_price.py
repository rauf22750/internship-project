# Generated by Django 5.1 on 2024-08-27 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0011_cartitem'),
    ]

    operations = [
    migrations.AddField(
        model_name='cartitem',
        name='total_price',
        field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
    ),
]
