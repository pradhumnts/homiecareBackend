# Generated by Django 4.0.6 on 2022-07-28 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0013_alter_qualification_degree'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isNurse',
            field=models.BooleanField(default=False),
        ),
    ]
