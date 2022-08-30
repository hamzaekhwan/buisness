# Generated by Django 3.2.15 on 2022-08-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20220828_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='addres',
            new_name='Bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='Email',
            field=models.EmailField(blank=True, max_length=70, unique=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Job',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='Name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]