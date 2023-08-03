# Generated by Django 4.2.3 on 2023-08-03 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_grupo_equipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('victorias', models.IntegerField(blank=True, default=None, null=True)),
                ('derrotas', models.IntegerField(blank=True, default=None, null=True)),
                ('empates', models.IntegerField(blank=True, default=None, null=True)),
                ('sancionado', models.BooleanField(blank=True, default=None, null=True)),
                ('partidosJugados', models.IntegerField(blank=True, default=None, null=True)),
                ('deporte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.deporte')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.equipo')),
                ('temporada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.temporada')),
            ],
        ),
    ]
