# Generated by Django 3.2.8 on 2021-11-09 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]