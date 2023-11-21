# Generated by Django 4.1.5 on 2023-11-20 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetails',
            old_name='fk_order_id',
            new_name='fk_order',
        ),
        migrations.RenameField(
            model_name='ordermaster',
            old_name='fk_customer_id',
            new_name='fk_customer',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='fk_product_id',
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='fk_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='food.foodproduct'),
        ),
        migrations.AddField(
            model_name='ordermaster',
            name='vchr_order_num',
            field=models.CharField(max_length=50, null=True),
        ),
    ]