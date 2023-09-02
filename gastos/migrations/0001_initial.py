# Generated by Django 4.2.2 on 2023-08-22 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cuentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('fecha_de_creacion', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripción', models.CharField(blank=True, max_length=200, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fecha', models.DateField()),
                ('fk_id_categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.categorias')),
                ('fk_id_perfil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gastos.cuentas')),
            ],
        ),
    ]