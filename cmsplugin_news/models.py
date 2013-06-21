import datetime
import os
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
import ckeditor.fields
from cms.models import CMSPlugin, Page
from cms.utils import get_cms_setting
from .utils import calculate_image_path

from cmsplugin_news import settings


class PublishedNewsManager(models.Manager):
    """
        Filters out all unpublished and items with a publication date in the future
    """
    def get_query_set(self):
        return super(PublishedNewsManager, self).get_query_set() \
                    .filter(is_published=True) \
                    .filter(pub_date__lte=datetime.datetime.now())


class News(CMSPlugin):
    """
    News
    """

    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), unique_for_date='pub_date',
                        help_text=_('A slug is a short name which uniquely identifies the news item for this day'))
    excerpt = models.TextField(_('Excerpt'), blank=True)
    content = models.TextField(_('Content'), blank=True)
    #content = ckeditor.fields.RichTextField(_('Content'), blank=True)
    news_picture = models.ImageField(_("image"), upload_to=calculate_image_path, max_length=255, null=True, blank=True)

    is_published = models.BooleanField(_('Published'), default=False)
    pub_date = models.DateTimeField(_('Publication date'), default=datetime.datetime.now)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    published = PublishedNewsManager()
    objects = models.Manager()
    
    def get_cover_picture_url(self, instance, filename):
        extension = os.path.splitext(filename)[1]
        normazed_path = re.compile('[ ]').sub('-', re.compile('[/:.()<>|?*]|(\\\)').sub('', instance.isbn))
        normalized_filename = os.path.join(str(instance.id) + '-' + normazed_path + extension)
        os.path.join('bestbill', normalized_filename)
        return self.cover_picture

    url = models.CharField(_("link"), max_length=255, blank=True, null=True,
        help_text=_("If present, clicking on image will take user to link."))
    
    page_link = models.ForeignKey(Page, verbose_name=_("page"), null=True,
        blank=True, help_text=_("If present, clicking on image will take user \
        to specified page."))
    

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if settings.LINK_AS_ABSOLUTE_URL and self.page_link:
            if settings.USE_LINK_ON_EMPTY_CONTENT_ONLY and not self.content:
                return self.page_link
        return reverse('news_detail', kwargs={'year': self.pub_date.strftime("%Y"),
                                    'month': self.pub_date.strftime("%m"),
                                    'day': self.pub_date.strftime("%d"),
                                    'slug': self.slug})
    def clean(self):
        if self.url and self.page_link:
            raise ValidationError(
                             _("You can enter a Link or a Page, but not both."))


class LatestNewsPlugin(CMSPlugin):
    """
        Model for the settings when using the latest news cms plugin
    """
    limit = models.PositiveIntegerField(_('Number of news items to show'),
                    help_text=_('Limits the number of items that will be displayed'))


class ArchiveNewsPlugin(CMSPlugin):
    """
        Modle for the settings when using news archives cms plugin
    """
    limit = models.PositiveIntegerField(_('Number of news items to show'),
                    help_text=_('Limits the number of items that will be displayed'))
     
     