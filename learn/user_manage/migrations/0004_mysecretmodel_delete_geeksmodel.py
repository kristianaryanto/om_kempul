# Generated by Django 4.1 on 2022-11-29 03:58

from django.db import migrations, models
import encrypted_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0003_geeksmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySecretModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('secret', encrypted_field.fields.EncryptedField()),
            ],
        ),
        migrations.DeleteModel(
            name='GeeksModel',
        ),
    ]
