# Generated by Django 5.2 on 2025-05-13 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='merchant_id',
            new_name='payment_intent',
        ),
    ]
