# Generated by Django 4.2.3 on 2023-08-16 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_jugador'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='estado',
            field=models.CharField(choices=[('en_juego', 'En juego'), ('finalizado', 'Finalizado'), ('pendiente', 'Pendiente')], default='pendiente', max_length=20),
        ),
    ]