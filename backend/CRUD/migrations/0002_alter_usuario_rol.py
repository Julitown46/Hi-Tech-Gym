# Generated by Django 5.2.1 on 2025-05-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('superuser', 'Superuser'), ('admin', 'Admin'), ('usuario', 'Usuario')], default='usuario', max_length=20),
        ),
    ]
