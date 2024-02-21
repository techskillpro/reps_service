# Generated by Django 5.0.1 on 2024-01-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Repair_App', '0012_alter_payment_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='static/images')),
                ('button_text', models.CharField(blank=True, max_length=50, null=True)),
                ('button_redirect_url', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
