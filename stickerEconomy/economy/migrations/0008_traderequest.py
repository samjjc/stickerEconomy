# Generated by Django 2.0.2 on 2018-03-08 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economy', '0007_auto_20180308_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_quantity', models.IntegerField(default=1)),
                ('given_quantity', models.IntegerField(default=1)),
                ('message', models.TextField(default='Hey, I want to make a trade.')),
                ('given_sticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given', to='economy.Sticker')),
                ('requested_sticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested', to='economy.Sticker')),
            ],
        ),
    ]