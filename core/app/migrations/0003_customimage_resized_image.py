# Generated by Django 4.2.22 on 2025-06-04 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_customimage_processed_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='resized_image',
            field=models.ImageField(blank=True, null=True, upload_to='resized/'),
        ),
    ]
