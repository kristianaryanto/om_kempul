# Generated by Django 4.1 on 2022-11-29 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0007_foobar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foobar',
            name='password',
            field=models.CharField(max_length=201),
        ),
        migrations.AlterField(
            model_name='foobar',
            name='user',
            field=models.CharField(max_length=201),
        ),
    ]