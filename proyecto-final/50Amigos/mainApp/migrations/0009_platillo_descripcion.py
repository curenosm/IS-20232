# Generated by Django 4.1.6 on 2023-05-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_platillo_ingredientes'),
    ]

    operations = [
        migrations.AddField(
            model_name='platillo',
            name='descripcion',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
