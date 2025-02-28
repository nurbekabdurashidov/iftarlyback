# Generated by Django 4.2.7 on 2025-02-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Enter full name', max_length=300, null=True, verbose_name='Full Name')),
                ('telegram_id', models.CharField(help_text='Enter telegram id', max_length=100, unique=True, verbose_name='Telegram ID')),
                ('language', models.CharField(choices=[('uz', "O'zbek"), ('en', 'English')], default='uz', help_text='Choose language', max_length=5, verbose_name='Language')),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Bot User',
                'verbose_name_plural': 'Bot Users',
            },
        ),
        migrations.CreateModel(
            name='TelegramChannelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(help_text='Enter channel id', max_length=150, unique=True, verbose_name='Channel ID')),
                ('channel_name', models.CharField(blank=True, help_text='Enter channel name', max_length=300, null=True, verbose_name='Channel Name')),
                ('channel_members_count', models.CharField(blank=True, help_text='Enter channel members count', max_length=200, null=True, verbose_name='Channel Memers Count')),
            ],
            options={
                'verbose_name': 'Telegram Channel',
                'verbose_name_plural': 'Telegram Channels',
            },
        ),
    ]
