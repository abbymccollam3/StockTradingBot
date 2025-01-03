# Generated by Django 5.1.3 on 2024-11-27 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_stockquote_raw_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockquote',
            name='raw_timestamp',
            field=models.CharField(blank=True, help_text='Non transformed timestamp string or int or float', max_length=120, null=True),
        ),
    ]
