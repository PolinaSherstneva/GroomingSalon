# Generated by Django 5.0.2 on 2024-02-20 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0004_alter_pet_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.TimeField(choices=[('9', '09:00'), ('10', '10:00'), ('11', '11:00'), ('12', '12:00'), ('13', '13:00'), ('14', '14:00'), ('15', '15:00'), ('16', '16:00'), ('17', '17:00')]),
        ),
    ]
