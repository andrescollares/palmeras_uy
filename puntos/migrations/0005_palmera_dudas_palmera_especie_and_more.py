# Generated by Django 5.2.3 on 2025-06-20 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puntos', '0004_alter_palmera_coords'),
    ]

    operations = [
        migrations.AddField(
            model_name='palmera',
            name='dudas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='palmera',
            name='especie',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='palmera',
            name='fecha_extraccion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='palmera',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='palmera',
            name='zona',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Monitoreo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('sintomas', models.TextField(blank=True, null=True)),
                ('palmera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitoreos', to='puntos.palmera')),
            ],
            options={
                'ordering': ['fecha'],
            },
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(max_length=200)),
                ('palmera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tratamientos', to='puntos.palmera')),
            ],
        ),
    ]
