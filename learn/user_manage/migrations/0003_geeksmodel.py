# Generated by Django 4.1 on 2022-11-29 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0002_rename_user_db_user_database'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeeksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geeks_field', models.BinaryField()),
            ],
        ),
    ]
