# Generated by Django 3.2 on 2021-05-16 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210517_0002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transaction',
            new_name='transaction_id',
        ),
    ]
