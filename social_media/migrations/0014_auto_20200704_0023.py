# Generated by Django 3.0.7 on 2020-07-04 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0013_remove_twitterapikey_what'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tumblrspider',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='tumblrspider',
            name='following',
        ),
        migrations.RemoveField(
            model_name='tumblrspider',
            name='user_profile_pictures',
        ),
    ]
