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
    BaseRangeVote = apps.get_model("buyersguide", "BaseRangeVote")

    for product in Product.objects.all():
        base_product = BaseProduct.objects.get(name=product.name)

        # Regenerate the votes:

        for vote in RangeVote.objects.filter(product=product):
            BaseRangeVote.objects.create(
                product=base_product,
                created_at=vote.created_at,
                attribute=vote.attribute,
                value=vote.value
            )

        for vote in BooleanVote.objects.filter(product=product):
            BaseBooleanVote.objects.create(
                product=base_product,
                created_at=vote.created_at,
                attribute=vote.attribute,
                value=vote.value
            )

        # Then regenerate the statistical records:

        range_vote = RangeProductVote.objects.get(product=product)
        (base_range_vote, brv_created) = BaseRangeProductVote.objects.get_or_create(
            product=base_product,
            defaults={
                'attribute': 'creepiness',
                'votes': 0,
                'average': 50
            }
        )
        base_range_vote.attribute = range_vote.attribute
        base_range_vote.votes = range_vote.votes
        base_range_vote.average = range_vote.average
        base_range_vote.save()

        for breakdown in RangeVoteBreakdown.objects.filter(product_vote=range_vote):
            (new_breakdown, created) = BaseRangeVoteBreakdown.objects.get_or_create(
                product_vote=base_range_vote
                )
            new_breakdown.count = breakdown.count
            new_breakdown.bucket = breakdown.bucket
            new_breakdown.save()

        boolean_vote = BooleanProductVote.objects.get(product=product)
        (base_boolean_vote, bbv_created) = BaseBooleanProductVote.objects.get_or_create(
            product=base_product,
            defaults={
                'attribute': 'confidence',
                'votes': 0
            }
        )
        base_boolean_vote.attributes = boolean_vote.attributes
        base_boolean_vote.votes = boolean_vote.votes
        base_boolean_vote.save()

        for breakdown in BooleanVoteBreakdown.objects.filter(product_vote=boolean_vote):
            (new_breakdown, created) = BaseBooleanVoteBreakdown.objects.get_or_create(
                product_vote=base_boolean_vote
            )
            new_breakdown.count = breakdown.count
            new_breakdown.bucket = breakdown.bucket
            new_breakdown.save()


class Migration(migrations.Migration):

    dependencies = [
        ('buyersguide', '0038_basebooleanproductvote_basebooleanvote_basebooleanvotebreakdown_baserangeproductvote_baserangevote_b'),
    ]

    operations = [
        migrations.RunPython(convertVotes, migrations.RunPython.noop),
    ]
