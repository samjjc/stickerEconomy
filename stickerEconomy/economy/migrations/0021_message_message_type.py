# Generated by Django 2.0.3 on 2018-03-22 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0020_room_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.IntegerField(default=1),
        ),
    ]
