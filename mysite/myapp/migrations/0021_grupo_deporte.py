# Generated by Django 4.2.3 on 2023-08-07 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_remove_grupo_deporte'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='deporte',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.deporte'),
        ),
    ]