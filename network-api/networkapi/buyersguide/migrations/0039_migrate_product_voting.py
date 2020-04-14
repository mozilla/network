# Generated by Django 2.2.12 on 2020-04-09 20:09

from django.db import migrations, models
import django.db.models.deletion
import networkapi.buyersguide.fields

def convertVotes(apps, schema_editor):
    Product = apps.get_model("buyersguide", "Product")
    BaseProduct = apps.get_model("buyersguide", "BaseProduct")

    # old voting types
    RangeProductVote = apps.get_model("buyersguide", "RangeProductVote")
    BooleanProductVote = apps.get_model("buyersguide", "BooleanProductVote")
    BooleanVoteBreakdown = apps.get_model("buyersguide", "BooleanVoteBreakdown")
    RangeVoteBreakdown = apps.get_model("buyersguide", "RangeVoteBreakdown")
    BooleanVote = apps.get_model("buyersguide", "BooleanVote")
    RangeVote = apps.get_model("buyersguide", "RangeVote")

    # new voting types
    BaseRangeProductVote = apps.get_model("buyersguide", "BaseRangeProductVote")
    BaseBooleanProductVote = apps.get_model("buyersguide", "BaseBooleanProductVote")
    BaseBooleanVoteBreakdown = apps.get_model("buyersguide", "BaseBooleanVoteBreakdown")
    BaseRangeVoteBreakdown = apps.get_model("buyersguide", "BaseRangeVoteBreakdown")
    BaseBooleanVote = apps.get_model("buyersguide", "BaseBooleanVote")
    BaseRangeVote = apps.get_model("buyersguide", "BaseRangeVote"),

    for product in Product.objects.all():
        base_product = BaseProduct.objects.get(name=product.name)

        # Regenerate the votes:

        for vote in RangeVote.objects.filter(product=product):
            BaseRangeVote.objects.create(
                created_at=vote.created_at,
                product=base_product,
                attribute=vote.attribute,
                bucket=vote.bucket
            )

        for vote in BooleanVote.objects.filter(product=product):
            BaseBooleanVote.objects.create(
                created_at=vote.created_at,
                product=base_product,
                attribute=vote.attribute,
                bucket=vote.bucket
            )

        # Then regenerate the statistical records:

        range_vote = RangeProductVote.objects.get(product=product)
        (base_range_vote, brv_created) = BaseRangeProductVote.objects.get_or_create(
            votes = range_vote.votes,
            attribute=range_vote.attribute,
            average=range_vote.average,
            product=base_product,
        )

        range_breakdown = RangeVoteBreakdown.objects.get(product=product)
        (base_range_breakdown, brb_created) = BaseRangeVoteBreakdown.objects.get_or_create(
            product_vote=base_range_vote,
            bucket=base_range_breakdown.bucket
        )

        boolean_vote = BooleanProductVote.objects.get(product=product)
        (base_boolean_vote, bbv_created) = BaseBooleanProductVote.objects.get_or_create(
            votes = boolean_vote.votes,
            attribute=boolean_vote.attribute,
            product=base_product,
        )

        boolean_breakdown = BooleanVoteBreakdown.objects.get(product=product)
        (base_boolean_breakdown, bbb_created) = BaseBooleanVoteBreakdown.objects.get_or_create(
            product_vote=base_boolean_vote,
            bucket=base_boolean_breakdown.bucket
        )


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0038_basebooleanproductvote_basebooleanvote_basebooleanvotebreakdown_baserangeproductvote_baserangevote_b'),
    ]

    operations = [
        migrations.RunPython(convertVotes, migrations.RunPython.noop),
    ]
