# Generated by Django 3.2 on 2023-07-06 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0028_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
