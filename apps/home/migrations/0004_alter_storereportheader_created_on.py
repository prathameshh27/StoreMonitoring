# Generated by Django 4.2.4 on 2023-08-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_storereportheader_staus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storereportheader',
            name='created_on',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
