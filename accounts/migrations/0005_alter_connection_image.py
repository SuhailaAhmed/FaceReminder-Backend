# Generated by Django 3.2 on 2023-06-20 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_connection_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='image',
            field=models.ImageField(upload_to='connections/'),
        ),
    ]
