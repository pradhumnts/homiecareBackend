# Generated by Django 4.0.6 on 2022-07-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0005_alter_message_user_from_alter_message_user_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
