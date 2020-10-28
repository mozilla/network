# Generated by Django 2.2.16 on 2020-10-21 00:00
import datetime

from django.db import migrations, models


def set_default_created_date(apps, schema_editor):
    # Update every Update instance to have a default created_date of Jan 1, 2020
    # But when a new model instance is created, assume auto_now=True
    Update = apps.get_model('buyersguide', 'Update')
    for update in Update.objects.all():
        update.created_date = datetime.datetime(2020, 1, 1, 0, 0)
        update.save()


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0004_auto_20201013_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True, help_text='The date this product was created'),
        ),
        migrations.RunPython(set_default_created_date),
        migrations.AlterField(
            model_name='update',
            name='created_date',
            field=models.DateField(auto_now_add=True, help_text='The date this product was created'),
        ),
    ]