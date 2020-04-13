# Generated by Django 2.2.12 on 2020-04-09 20:09

from django.db import migrations, models
import django.db.models.deletion
import networkapi.buyersguide.fields


def convertProducts(apps, schema_editor):
    Product = apps.get_model("buyersguide", "Product")
    BaseProduct = apps.get_model("buyersguide", "BaseProduct")
    GeneralProduct = apps.get_model("buyersguide", "GeneralProduct")
    ProductPrivacyPolicyLink = apps.get_model("buyersguide", "ProductPrivacyPolicyLink")
    BaseProductPrivacyPolicyLink = apps.get_model("buyersguide", "BaseProductPrivacyPolicyLink")

    # Recreate products
    for product in Product.objects.all():
        (general, created) = GeneralProduct.objects.get_or_create(
            # base fields
            draft=product.draft,
            adult_content=product.adult_content,
            review_date=product.review_date,
            name=product.name,
            slug=product.slug,
            company=product.company,
            blurb=product.blurb,
            url=product.url,
            price=product.price,
            image=product.image,
            cloudinary_image=product.cloudinary_image,
            meets_minimum_security_standards=product.meets_minimum_security_standards,
            share_data=product.share_data,
            share_data_helptext=product.share_data_helptext,
            how_does_it_share=product.how_does_it_share,
            user_friendly_privacy_policy=product.user_friendly_privacy_policy,
            user_friendly_privacy_policy_helptext=product.user_friendly_privacy_policy_helptext,
            worst_case=product.worst_case,
            phone_number=product.phone_number,
            live_chat=product.live_chat,
            email=product.email,
            twitter=product.twitter,
            # general fields
            uses_encryption=product.uses_encryption,
            uses_encryption_helptext=product.uses_encryption_helptext,
            security_updates=product.security_updates,
            security_updates_helptext=product.security_updates_helptext,
            strong_password=product.strong_password,
            strong_password_helptext=product.strong_password_helptext,
            manage_vulnerabilities=product.manage_vulnerabilities,
            manage_vulnerabilities_helptext=product.manage_vulnerabilities_helptext,
            privacy_policy=product.privacy_policy,
            privacy_policy_helptext=product.privacy_policy_helptext,
            camera_device=product.camera_device,
            camera_app=product.camera_app,
            microphone_device=product.microphone_device,
            microphone_app=product.microphone_app,
            location_device=product.location_device,
            location_app=product.location_app,
            delete_data=product.delete_data,
            delete_data_helptext=product.delete_data_helptext,
            parental_controls=product.parental_controls,
            child_rules_helptext=product.child_rules_helptext,
            collects_biometrics=product.collects_biometrics,
            collects_biometrics_helptext=product.collects_biometrics_helptext,
        )

        if created:
            for cat in product.product_category.all():
                general.product_category.add(cat)

            for update in product.updates.all():
                general.updates.add(update)

            general.save()

    # After performing all the conversions, cross-link the related products
    for product in Product.objects.all():
        base = BaseProduct.objects.get(name=product.name)
        for related in product.related_products.all():
            related_base_product = BaseProduct.objects.get(name=related.name)
            base.related_products.add(related_base_product)

    # Recreate the privacy link objects
    for link in ProductPrivacyPolicyLink.objects.all():
        product = Product.objects.get(pk=link.product.pk)
        general = BaseProduct.objects.get(name=product.name)
        (newlink, created) = BaseProductPrivacyPolicyLink.objects.get_or_create(
            product=general,
            label=link.label,
            url=link.url,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0035_baseproduct_generalproduct'),
    ]

    operations = [
         migrations.RunPython(convertProducts, migrations.RunPython.noop),
    ]
