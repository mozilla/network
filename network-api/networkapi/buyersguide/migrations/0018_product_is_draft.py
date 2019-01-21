# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-09 20:20
from __future__ import unicode_literals

from django.db import migrations, models

def publish_all_products_up_to_now(apps, schema_editor):
    """
    Ensure that any product that was created prior to having
    a "draft" flag gets marked as not a draft at all.
    """
    Product = apps.get_model("buyersguide", "Product")

    for product in Product.objects.all():
        product.draft = False;
        product.save();


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0017_auto_20181114_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='draft',
            field=models.BooleanField(default=True, help_text='When checked, this product will only show for CMS-authenticated users'),
        ),
        migrations.RunPython(publish_all_products_up_to_now, migrations.RunPython.noop),
    ]
