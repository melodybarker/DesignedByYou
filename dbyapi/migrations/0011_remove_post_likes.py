# Generated by Django 4.0.3 on 2022-03-18 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbyapi', '0010_remove_diyuser_following_diyuser_following_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]