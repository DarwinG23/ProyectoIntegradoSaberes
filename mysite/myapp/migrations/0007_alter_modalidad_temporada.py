# Generated by Django 4.2.3 on 2023-08-03 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_modalidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalidad',
            name='temporada',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.temporada'),
        ),
    ]
