# Generated by Django 4.2.5 on 2023-10-04 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='xipcode',
            new_name='zipcode',
        ),
    ]