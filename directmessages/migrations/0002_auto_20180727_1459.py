# Generated by Django 2.0.7 on 2018-07-27 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('directmessages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='sent at'),
            preserve_default=False,
        ),
    ]
