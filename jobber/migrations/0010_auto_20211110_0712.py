# Generated by Django 3.2.8 on 2021-11-10 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobber', '0009_alter_resume_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cover_letter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobber.coverletter'),
        ),
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jobber.resume'),
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
