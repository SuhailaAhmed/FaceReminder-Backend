# Generated by Django 3.2 on 2023-03-14 12:03

# import Gp_Backend.s3_storages
from django.db import migrations, models

import accounts.models.connection


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    # operations = [
    #     migrations.AlterField(
    #         model_name='connection',
    #         name='image',
    #         field=models.ImageField(storage=Gp_Backend.s3_storages.MediaStorage, upload_to=accounts.models.connection.get_image_path),
    #     ),
    # ]
