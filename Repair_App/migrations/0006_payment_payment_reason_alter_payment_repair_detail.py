# Generated by Django 5.0.1 on 2024-01-26 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Repair_App', '0005_complain_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='repair_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Repair_App.repair_details'),
        ),
    ]