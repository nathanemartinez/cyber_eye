# Generated by Django 3.0.7 on 2020-07-04 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0011_auto_20200704_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitterapikey',
            name='what',
            field=models.CharField(default='', max_length=200),
        ),
    ]
