# Generated by Django 5.0.2 on 2024-05-13 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0016_remove_race_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='type',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='Salon.typeanimal'),
        ),
    ]
