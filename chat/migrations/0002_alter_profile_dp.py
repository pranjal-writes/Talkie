# Generated by Django 4.2.2 on 2023-07-19 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(default='blank-picture.png', upload_to='profile_pics'),
        ),
    ]
