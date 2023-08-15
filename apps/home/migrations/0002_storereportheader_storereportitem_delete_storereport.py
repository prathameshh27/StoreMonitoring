# Generated by Django 4.2.4 on 2023-08-12 15:33

import apps.utils.functions
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreReportHeader',
            fields=[
                ('created_on', models.DateTimeField(auto_created=True)),
                ('id', models.CharField(default=apps.utils.functions.custom_id, editable=False, max_length=25, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StoreReportItem',
            fields=[
                ('id', models.CharField(default=apps.utils.functions.custom_id, editable=False, max_length=25, primary_key=True, serialize=False, unique=True)),
                ('uptime_last_hour', models.IntegerField(blank=True, null=True)),
                ('uptime_last_day', models.IntegerField(blank=True, null=True)),
                ('update_last_week', models.IntegerField(blank=True, null=True)),
                ('downtime_last_hour', models.IntegerField(blank=True, null=True)),
                ('downtime_last_day', models.IntegerField(blank=True, null=True)),
                ('downtime_last_week', models.IntegerField(blank=True, null=True)),
                ('report_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_items', to='home.storereportheader')),
                ('store_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_report', to='home.store')),
            ],
        ),
        migrations.DeleteModel(
            name='StoreReport',
        ),
    ]
