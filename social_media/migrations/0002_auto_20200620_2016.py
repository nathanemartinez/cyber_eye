# Generated by Django 3.0.7 on 2020-06-21 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterspider',
            name='user_info',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
