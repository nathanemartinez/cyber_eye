# Generated by Django 3.0.7 on 2020-07-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0025_auto_20200710_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterspider',
            name='followers',
            field=models.CharField(blank=True, default='social_media/media/social_media/twitter/followers/default.txt', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='twitterspider',
            name='following',
            field=models.CharField(blank=True, default='social_media/media/social_media/twitter/following/default.txt', max_length=200, null=True),
        ),
    ]
