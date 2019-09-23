# Generated by Django 2.2.4 on 2019-09-12 16:31

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0078_blogpagecategory_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='category',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, help_text='Which blog categories is this blog page associated with?', to='wagtailpages.BlogPageCategory', verbose_name='Categories'),
        ),
    ]
