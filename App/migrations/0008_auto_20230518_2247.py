# Generated by Django 3.2 on 2023-05-18 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='promo_code',
        ),
        migrations.AddField(
            model_name='coupon',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='code',
            field=models.CharField(default='Code', max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
