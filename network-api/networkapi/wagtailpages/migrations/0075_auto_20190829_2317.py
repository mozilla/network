# Generated by Django 2.2.4 on 2019-08-29 23:17

from django.db import migrations



from django.db import migrations, models

def add_blog_category(apps, schema_editor):
    BlogPageCategory = apps.get_model("wagtailpages", "BlogPageCategory")

    mozfest_festival = BlogPageCategory(name='Mozilla Festival')
    mozfest_festival.save()

    open_leadership_and_events = BlogPageCategory(name='Open Leadership & Events')
    open_leadership_and_events.save()

    internet_health = BlogPageCategory(name='Internet Health')
    internet_health.save()

    fellowships_and_awards = BlogPageCategory(name='Fellowships & Awards')
    fellowships_and_awards.save()

    advocacy = BlogPageCategory(name='Advocacy')
    advocacy.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailpages', '0074_blogpagecategory'),
    ]

    operations = [
        migrations.RunPython(add_blog_category),
    ]
