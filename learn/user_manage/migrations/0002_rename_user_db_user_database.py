# Generated by Django 4.1 on 2022-11-28 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_db',
            new_name='user_database',
        ),
    ]