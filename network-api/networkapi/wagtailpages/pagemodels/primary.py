from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from .base_fields import base_fields
from .mixin.foundation_metadata import FoundationMetadataPageMixin
from ..utils import (
    set_main_site_nav_information,
    get_page_tree_information,
)


class PrimaryPage(FoundationMetadataPageMixin, Page):
    """
    Basically a straight copy of modular page, but with
    restrictions on what can live 'under it'.

    Ideally this is just PrimaryPage(ModularPage) but
    setting that up as a migration seems to be causing
    problems.
    """
    header = models.CharField(
        max_length=250,
        blank=True
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_banner',
        verbose_name='Hero Image',
        help_text='Choose an image that\'s bigger than 4032px x 1152px with aspect ratio 3.5:1',
    )

    def get_banner(self):
        if self.banner is None:
            # note: we need to reverse get_ancestors, because by default
            # this gives a list that starts at the root, and then gets more
            # specific, ending in the direct parent. We want to check in the
            # opposite direction: start at the parent until we hit the root.
            ancestors = self.get_ancestors().reverse()
            for page in ancestors:
                page = page.specific
                valid = isinstance(page, PrimaryPage)
                if valid and page.banner is not None:
                    return page.banner

        return self.banner

    intro = models.CharField(
        max_length=250,
        blank=True,
        help_text='Intro paragraph to show in hero cutout box'
    )

    narrowed_page_content = models.BooleanField(
        default=False,
        help_text='For text-heavy pages, turn this on to reduce the overall width of the content on the page.'
    )

    zen_nav = models.BooleanField(
        default=False,
        help_text='For secondary nav pages, use this to collapse the primary nav under a toggle hamburger.'
    )

    body = StreamField(base_fields)

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
          [
            FieldPanel('narrowed_page_content'),
          ],
          classname="collapsible"
        ),
        MultiFieldPanel(
          [
            FieldPanel('zen_nav'),
          ],
          classname="collapsible"
        )
    ]

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        ImageChooserPanel('banner'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

    subpage_types = [
        'PrimaryPage',
        'RedirectingPage',
        'BanneredCampaignPage'
    ]

    show_in_menus_default = True

    def get_context(self, request):
        context = super().get_context(request)
        context = set_main_site_nav_information(self, context, 'Homepage')
        context = get_page_tree_information(self, context)
        return context
