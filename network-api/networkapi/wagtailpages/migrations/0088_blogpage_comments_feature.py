# Generated by Django 2.2.5 on 2019-11-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0087_auto_20191003_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='comments_feature',
            field=models.BooleanField(default=False, help_text='Check box to add comments feature for this blog post.'),
        ),
    ]
