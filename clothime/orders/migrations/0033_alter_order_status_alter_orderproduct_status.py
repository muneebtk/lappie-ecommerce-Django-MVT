# Generated by Django 4.0.4 on 2023-09-05 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_alter_order_status_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('Delivered', 'Delivered'), ('shipped', 'shipped'), ('cancelled', 'cancelled')], default='new', max_length=10),
        ),
    ]