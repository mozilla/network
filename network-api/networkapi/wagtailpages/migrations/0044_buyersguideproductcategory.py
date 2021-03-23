# Generated by Django 2.2.17 on 2021-03-03 17:28

import django
from django.db import migrations, models
import networkapi.buyersguide.utils


def copy_buyersguide_product_categories(apps, schema_editor):
    OldBuyersGuideProductCategory = apps.get_model("buyersguide", "BuyersGuideProductCategory")
    NewBuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")

    for cat in OldBuyersGuideProductCategory.objects.all().order_by('id'):
        NewBuyersGuideProductCategory.objects.create(
            name=cat.name,
            description=cat.description,
            featured=cat.featured,
            hidden=cat.hidden,
            slug=cat.slug,
            sort_order=cat.sort_order,
            og_image=cat.og_image
        )


def remove_new_buyersguide_product_categories(apps, schema_editor):
    NewBuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")
    NewBuyersGuideProductCategory.objects.all().delete()


def find_and_copy_old_product_category_to_model(apps, schema_editor):
    ProductPageCategory = apps.get_model("wagtailpages", "ProductPageCategory")
    BuyersGuideProductCategory = apps.get_model("wagtailpages", "BuyersGuideProductCategory")
    for product_page_category in ProductPageCategory.objects.all():
        if hasattr(product_page_category, 'category'):
            category = product_page_category.category
            # Find the "new" model instance of the old category. Make sure
            # there is only one returned, not a full QuerySet
            new_category = BuyersGuideProductCategory.objects.filter(name=category.name).first()
            # Assign the new temporary "category_new" field. This will be
            # renamed later
            product_page_category.category_new = new_category
            product_page_category.save()


def reverse_find_and_copy_old_product_category_to_model(apps, schema_editor):
    ProductPageCategory = apps.get_model("wagtailpages", "ProductPageCategory")
    for product_page_category in ProductPageCategory.objects.all():
        product_page_category.category_new = None
        product_page_category.save()


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0008_auto_20210126_1943'),
        ('wagtailpages', '0043_add_single_image_block_to_articles'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyersGuideProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description of the product category. Max. 300 characters.', max_length=300)),
                ('featured', models.BooleanField(default=False, help_text="Featured category will appear first on Buyer's Guide site nav")),
                ('hidden', models.BooleanField(default=False, help_text="Hidden categories will not appear in the Buyer's Guide site nav at all")),
                ('slug', models.SlugField(blank=True, help_text='A URL-friendly version of the category name. This is an auto-generated field.')),
                ('sort_order', models.IntegerField(default=1, help_text='Sort ordering number. Same-numbered items sort alphabetically')),
                ('og_image', models.FileField(blank=True, help_text='Image to use as OG image', max_length=2048, upload_to=networkapi.buyersguide.utils.get_category_og_image_upload_path)),
            ],
            options={
                'verbose_name': 'Buyers Guide Product Category',
                'verbose_name_plural': 'Buyers Guide Product Categories',
                'ordering': ['sort_order', 'name'],
            },
        ),
        # Copy all BuyersGuideProductCategory's to the new app
        migrations.RunPython(copy_buyersguide_product_categories, remove_new_buyersguide_product_categories),
        # Create a duplicate field for housing the new BuyersGuideProductCategory
        migrations.AddField(
            model_name='productpagecategory',
            name='category_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailpages.BuyersGuideProductCategory'),
        ),
        # Find the "old" product category's "clone" (the new model) and add it to `category_new`
        migrations.RunPython(find_and_copy_old_product_category_to_model, reverse_find_and_copy_old_product_category_to_model),
    ]
