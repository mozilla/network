# Generated by Django 2.2.16 on 2020-10-26 22:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0006_auto_20201015_1607'),
        ('wagtailpages', '0013_productpage_types'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productpage',
            old_name='url',
            new_name='product_url',
        ),
        migrations.AlterField(
            model_name='productpage',
            name='review_date',
            field=models.DateField(help_text='Review date of this product', null=True),
        ),
        migrations.CreateModel(
            name='RelatedProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_product_pages', to='wagtailpages.ProductPage')),
                ('related_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailpages.ProductPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductUpdates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_updates', to='wagtailpages.ProductPage')),
                ('update', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='buyersguide.Update')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPagePrivacyPolicyLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='Label for this link on the product page', max_length=500)),
                ('url', models.URLField(blank=True, help_text='Privacy policy URL', max_length=2048)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_privacy_policy_links', to='wagtailpages.ProductPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='buyersguide.BuyersGuideProductCategory')),
                ('product', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', to='wagtailpages.ProductPage')),
            ],
            options={
                'verbose_name': 'Product Page Category',
            },
        ),
    ]
