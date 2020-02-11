# Generated by Django 2.0.7 on 2018-07-28 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('directmessages', '0002_auto_20180727_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatroom_receiver', to=settings.AUTH_USER_MODEL, verbose_name='Recipient')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatroom_sender', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-sent_at']},
        ),
    ]