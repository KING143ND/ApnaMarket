# Generated by Django 3.2 on 2023-05-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_alter_customer_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(choices=[('Home', 'Home'), ('Work', 'Work')], max_length=15),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Not Specified', 'Not Specified')], max_length=15),
        ),
    ]
