# Generated by Django 5.2 on 2025-05-15 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_order_is_paid_order_status_order_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_intent',
            new_name='merchant_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
