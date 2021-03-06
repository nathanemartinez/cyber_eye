# Generated by Django 3.0.7 on 2020-07-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0018_auto_20200708_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterspider',
            name='followers',
            field=models.FileField(blank=True, null=True, upload_to='social_media/media/social_media/twitter/followers/default.txt'),
        ),
        migrations.AlterField(
            model_name='twitterspider',
            name='following',
            field=models.FileField(blank=True, null=True, upload_to='social_media/media/social_media/twitter/following/default.txt'),
        ),
    ]
