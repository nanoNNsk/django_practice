# Generated by Django 5.1.4 on 2025-01-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
