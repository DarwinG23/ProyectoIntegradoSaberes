# Generated by Django 4.2.3 on 2023-08-14 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_alter_competidor_options_alter_competidor_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.equipo')),
                ('temporada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.temporada')),
            ],
        ),
    ]
