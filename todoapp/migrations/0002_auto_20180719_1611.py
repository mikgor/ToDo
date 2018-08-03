# Generated by Django 2.0.7 on 2018-07-19 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='show',
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]