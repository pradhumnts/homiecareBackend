# Generated by Django 4.0.6 on 2022-08-04 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0017_message_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='nurse',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]