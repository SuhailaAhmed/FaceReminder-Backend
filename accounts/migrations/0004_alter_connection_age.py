# Generated by Django 3.2 on 2023-03-21 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230314_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='age',
            field=models.PositiveIntegerField(default=18),
        ),
    ]