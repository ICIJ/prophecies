# Generated by Django 3.2.6 on 2021-08-30 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tip'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tip',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
