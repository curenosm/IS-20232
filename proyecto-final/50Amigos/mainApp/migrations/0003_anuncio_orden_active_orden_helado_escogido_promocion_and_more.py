# Generated by Django 4.1.6 on 2023-05-10 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_orden_options_pedido_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.TextField(max_length=200)),
                ('anunciante', models.TextField(max_length=200)),
                ('valido_hasta', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='orden',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='helado_escogido',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='mainApp.platillo'),
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('codigo', models.UUIDField(auto_created=True, unique=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.TextField(max_length=500)),
                ('valido_hasta', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('platillo', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='mainApp.platillo')),
            ],
            options={
                'verbose_name': 'Promocion',
                'verbose_name_plural': 'Promociones',
            },
        ),
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('codigo', models.UUIDField(auto_created=True, unique=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('promocion', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='mainApp.promocion')),
            ],
            options={
                'verbose_name': 'Cupon',
                'verbose_name_plural': 'Cupones',
            },
        ),
    ]
