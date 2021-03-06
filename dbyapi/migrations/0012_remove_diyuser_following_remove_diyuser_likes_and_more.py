# Generated by Django 4.0.3 on 2022-03-19 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbyapi', '0011_remove_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diyuser',
            name='following',
        ),
        migrations.RemoveField(
            model_name='diyuser',
            name='likes',
        ),
        migrations.AddField(
            model_name='diyuser',
            name='follows',
            field=models.ManyToManyField(to='dbyapi.diyuser'),
        ),
        migrations.RemoveField(
            model_name='following',
            name='from_diyuser',
        ),
        migrations.AddField(
            model_name='following',
            name='from_diyuser',
            field=models.ManyToManyField(related_name='from_diyuser', to='dbyapi.diyuser'),
        ),
        migrations.RemoveField(
            model_name='following',
            name='to_diyuser',
        ),
        migrations.AddField(
            model_name='following',
            name='to_diyuser',
            field=models.ManyToManyField(to='dbyapi.diyuser'),
        ),
    ]
