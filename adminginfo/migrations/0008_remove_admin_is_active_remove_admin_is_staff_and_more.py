# Generated by Django 5.1.7 on 2025-05-05 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminginfo', '0007_admin_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='is_superuser',
        ),
    ]
