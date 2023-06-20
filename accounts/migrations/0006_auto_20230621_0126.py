# Generated by Django 3.2 on 2023-06-20 22:26

import accounts.models.connection
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_connection_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='connection',
            name='image',
            field=models.ImageField(upload_to=accounts.models.connection.get_image_folder_path),
        ),
    ]
