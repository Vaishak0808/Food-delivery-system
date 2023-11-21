# Generated by Django 4.1.5 on 2023-11-18 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='address',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='alt_phone_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='fk_role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.role'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]