# Generated by Django 4.2.2 on 2023-08-22 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gastos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gastos',
            old_name='fk_id_perfil',
            new_name='fk_id_cuenta',
        ),
    ]
