from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


@register_snippet
class ProductPrivacyPolicyLink(Orderable, models.Model):

    label = models.CharField(
        max_length=500,
        help_text='Label for this link on the product page'
    )

    url = models.URLField(
        max_length=2048,
        help_text='Privacy policy URL',
        blank=True
    )

    def __str__(self):
        return f'{self.product.name}: {self.label} ({self.url})'

    class Meta:
        verbose_name = "Buyers Guide Product Privacy Policy link"
        verbose_name_plural = "Buyers Guide Product Privacy Policy links"
        app_label = "buyersguide"
