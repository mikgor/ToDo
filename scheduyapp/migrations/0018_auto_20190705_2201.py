# Generated by Django 2.0.7 on 2019-07-05 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduyapp', '0017_task_notification_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scheduyapp.Notification', verbose_name='Notification'),
        ),
    ]
