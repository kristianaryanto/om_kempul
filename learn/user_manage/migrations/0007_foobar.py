# Generated by Django 4.1 on 2022-11-29 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0006_delete_foobar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foobar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=101)),
                ('password', models.CharField(max_length=101)),
            ],
        ),
    ]