# Generated by Django 4.1.7 on 2023-04-24 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_message_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Phone_Number',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
