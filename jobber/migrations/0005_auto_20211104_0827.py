# Generated by Django 3.2.8 on 2021-11-04 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('jobber', '0004_auto_20211024_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='user',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='user',
        ),
        migrations.RemoveField(
            model_name='coverletter',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='user',
        ),
        migrations.RemoveField(
            model_name='resume',
            name='user',
        ),
        migrations.AddField(
            model_name='application',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coverletter',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opportunity',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='profile',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
