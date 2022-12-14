# Generated by Django 4.0.6 on 2022-07-17 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0003_address_create_at_address_updated_at_nurse_create_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(max_length=2000)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
