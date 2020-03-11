from .index import IndexPage


class CampaignIndexPage(IndexPage):
    """
    The campaign index is specifically for campaign pages
    """

    subpage_types = [
        'BanneredCampaignPage',
        'CampaignPage',
    ]

    template = 'wagtailpages/index_page.html'
