# Generated by Django 3.2.8 on 2021-10-24 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobber', '0002_auto_20211024_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='recruiter_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_contact', to='jobber.contact'),
        ),
    ]