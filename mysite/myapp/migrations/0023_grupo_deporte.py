# Generated by Django 4.2.3 on 2023-08-07 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_remove_grupo_deporte'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='deporte',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.deporte'),
        ),
    ]
