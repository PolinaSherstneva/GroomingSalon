# Generated by Django 5.0.2 on 2024-04-30 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0013_race_alter_record_status_portfolio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.race'),
        ),
    ]
