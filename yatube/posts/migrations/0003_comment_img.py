# Generated by Django 3.1.7 on 2021-03-10 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_delete_disk'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='comments/'),
        ),
    ]