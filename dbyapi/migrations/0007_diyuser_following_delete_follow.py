# Generated by Django 4.0.3 on 2022-03-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbyapi', '0006_alter_follow_follower_alter_follow_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='diyuser',
            name='following',
            field=models.ManyToManyField(related_name='followed_by', to='dbyapi.diyuser'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
