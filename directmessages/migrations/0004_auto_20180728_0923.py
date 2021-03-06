# Generated by Django 2.0.7 on 2018-07-28 09:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('directmessages', '0003_auto_20180728_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='sent at'),
            preserve_default=False,
        ),
    ]
