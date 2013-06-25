from cmsplugin_news.forms import NewsForm
from cmsplugin_news.models import News
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext
from django.db import models
from django import forms



class NewsAdmin(admin.ModelAdmin):
    """
        Admin for news
    """
    date_hierarchy = 'pub_date'
    list_display = ('slug', 'title', 'is_published', 'show_in_carousel','show_in_newsarchive', 'news_picture', 'page_link', 'pub_date')
    #list_editable = ('title', 'is_published')
    list_filter = ('is_published', )
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
  
    actions = ['make_published', 'make_unpublished']

    save_as = True
    save_on_top = True
    
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
    class Media:
        js = ('/media/ckeditor/ckeditor.js',) # The , at the end of this list IS important.
  
    
    def queryset(self, request):
        """
            Override to use the objects and not just the default visibles only.
        """
        return News.objects.all()

    def make_published(self, request, queryset):
        """
            Marks selected news items as published
        """
        rows_updated = queryset.update(is_published=True)
        self.message_user(request, ungettext('%(count)d newsitem was published',
                                            '%(count)d newsitems were published',
                                            rows_updated) % {'count': rows_updated})
    make_published.short_description = _('Publish selected news')

    def make_unpublished(self, request, queryset):
        """
            Marks selected news items as unpublished
        """
        rows_updated = queryset.update(is_published=False)
        self.message_user(request, ungettext('%(count)d newsitem was unpublished',
                                            '%(count)d newsitems were unpublished',
                                            rows_updated) % {'count': rows_updated})
    make_unpublished.short_description = _('Unpublish selected news')

admin.site.register(News, NewsAdmin)
