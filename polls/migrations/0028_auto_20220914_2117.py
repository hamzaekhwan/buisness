# Generated by Django 3.2.15 on 2022-09-14 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_auto_20220914_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='color',
            new_name='color1',
        ),
        migrations.AddField(
            model_name='data',
            name='color2',
            field=models.CharField(blank=True, default='#0000FF', max_length=50, null=True),
        ),
    ]