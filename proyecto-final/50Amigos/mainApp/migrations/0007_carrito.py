# Generated by Django 4.1.6 on 2023-05-13 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_anuncio_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('orden', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carrito', to='mainApp.orden')),
            ],
        ),
    ]
