# Generated by Django 5.1.2 on 2024-10-26 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_dangerarea_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dangerarea',
            old_name='type',
            new_name='danger_type',
        ),
    ]