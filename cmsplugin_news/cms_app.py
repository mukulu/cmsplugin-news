from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from cmsplugin_news.menu import NewsItemMenu


class NewsAppHook(CMSApp):
    name = _('News App')
    urls = ['news.urls']
    menus = [NewsItemMenu]


apphook_pool.register(NewsAppHook)
