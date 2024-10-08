# Generated by Django 4.2.9 on 2024-07-30 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0002_product_picture1_product_picture2_product_picture3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='product',
            name='picture1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='picture2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='picture3',
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='final.product')),
            ],
        ),
    ]
