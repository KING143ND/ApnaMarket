# Generated by Django 3.2 on 2023-05-15 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zipcode',
            field=models.IntegerField(max_length=6),
        ),
    ]
