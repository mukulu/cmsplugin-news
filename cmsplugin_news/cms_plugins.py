from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_news.models import LatestNewsPlugin, News, ArchiveNewsPlugin
from cmsplugin_news import settings


class CMSLatestNewsPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = LatestNewsPlugin
    name = _('Latest news')
    render_template = "news/latest_news.html"

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        latest = News.published.all().order_by('pub_date')[:instance.limit]
        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
        })
        return context

if not settings.DISABLE_LATEST_NEWS_PLUGIN:
    plugin_pool.register_plugin(CMSLatestNewsPlugin)

class CMSArchiveNewsPlugin(CMSPluginBase):
    """
        Plugin class for the news archive
    """
    model = ArchiveNewsPlugin
    name = _('News Archives')
    render_template = "news/news_archive_custom.html"

    def render(self, context, instance, placeholder):
        """
            Render archive news
        """
        news = News.published.all()
        context.update({
            'instance': instance,
            'news': news,
            'pages' : instance.limit if instance.limit > 0 else 1,
            'placeholder': placeholder,
        })
        return context
plugin_pool.register_plugin(CMSArchiveNewsPlugin)
