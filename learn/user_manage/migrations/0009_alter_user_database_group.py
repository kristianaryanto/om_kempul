# Generated by Django 4.1 on 2022-11-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0008_alter_foobar_password_alter_foobar_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_database',
            name='group',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]