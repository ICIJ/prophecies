# Generated by Django 3.2.9 on 2022-01-13 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20220110_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='recordLinkTemplate',
            new_name='record_link_template',
        ),
    ]