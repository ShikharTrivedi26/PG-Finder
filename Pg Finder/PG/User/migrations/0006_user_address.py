# Generated by Django 4.1.7 on 2023-04-24 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Address',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]
