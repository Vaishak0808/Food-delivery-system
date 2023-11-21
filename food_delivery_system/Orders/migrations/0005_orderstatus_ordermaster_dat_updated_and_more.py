# Generated by Django 4.1.5 on 2023-11-20 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_userdetails_int_type'),
        ('Orders', '0004_alter_ordermaster_dbl_total_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vchr_status', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='ordermaster',
            name='dat_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordermaster',
            name='fk_delivery_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_details', to='login.userdetails'),
        ),
        migrations.AddField(
            model_name='ordermaster',
            name='fk_updated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_id', to='login.userdetails'),
        ),
        migrations.AlterField(
            model_name='ordermaster',
            name='fk_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_details', to='login.userdetails'),
        ),
        migrations.AddField(
            model_name='ordermaster',
            name='fk_order_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Orders.orderstatus'),
        ),
    ]
