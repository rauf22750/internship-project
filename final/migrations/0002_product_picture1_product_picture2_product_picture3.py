# Generated by Django 4.2.9 on 2024-07-30 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='picture2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='picture3',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
