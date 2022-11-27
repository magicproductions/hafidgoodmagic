from abc import ABC

from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django_extensions.db.fields import AutoSlugField

from rest_framework.fields import Field

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)

from wagtail.api import APIField
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from streams import blocks


class ImageSerializedField(Field, ABC):
    def to_representation(self, value):
        return {
            'url'   : value.file.url,
            'title' : value.title,
            'width' : value.width,
            'height': value.height,
        }


class BlogAuthorsOrderable(Orderable):
    """Allows users to select one or more authors"""
    
    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )
    
    panels = [
        FieldPanel('author'),
    ]
    
    # These are properties to return data for API requests
    @property
    def author_name(self):
        return self.author.name
    
    @property
    def author_email(self):
        return self.author.email
    
    @property
    def author_image(self):
        return self.author.image
    
    api_fields = [
        APIField('author'),
        APIField('author_name'),
        APIField('author_email'),
        APIField('author_image', serializer=ImageSerializedField()),
    ]


class BlogAuthor(models.Model):
    """Blog author for SnippetChooserPanel"""
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+',
    )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('email'),
                FieldPanel('image'),
            ],
            heading=_('Name and Image'),
        )
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Blog Author')
        verbose_name_plural = _('Blog Authors')


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from='name',
        verbose_name='slug',
        editable=True,
        allow_unicode=True,
        max_length=150,
        help_text=_('A slug to identify posts by this category.')
    )
    
    panels = [
        FieldPanel(_('name')),
        FieldPanel(_('slug')),
    ]
    
    class Meta:
        verbose_name = _('Blog Category')
        verbose_name_plural = _('Blog Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


register_snippet(BlogCategory)


# class BlogTag(models.Model):
#     name = models.CharField(max_length=100)
#     slug = AutoSlugField(
#         populate_from='name',
#         verbose_name='slug',
#         editable=True,
#         allow_unicode=True,
#         max_length=150,
#         help_text=_('A slug to identify posts by this tag.')
#     )
#
#     panels = [
#         FieldPanel(_('name')),
#         FieldPanel(_('slug')),
#     ]
#
#     class Meta:
#         verbose_name = _('Blog Tag')
#         verbose_name_plural = _('Blog Tags')
#         ordering = ['name']
#
#     def __str__(self):
#         return self.name
#
#
# register_snippet(BlogTag)


class BlogListingPage(RoutablePageMixin, Page):
    template = 'blog/blog_listing_page.html'
    ajax_template = 'blog/blog_ajax.html'
    max_count = 1
    subpage_types = [
        'blog.VideoBlogPage',
        'blog.ArticleBlogPage',
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        
        paginator = Paginator(all_posts, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        context['posts'] = posts
        
        context['authors'] = BlogAuthor.objects.all()
        context['categories'] = BlogCategory.objects.all()
        # context['tags'] = BlogTag.objects.all()
        return context
    
    @route(r'^category/(?P<cat_slug>[-\w]*)/$', name='category_view')
    def category_view(self, request, cat_slug):
        """Find Blog post based on category."""
        context = self.get_context(request)
        
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None
        
        if category is None:
            pass
        
        context['posts'] = BlogDetailPage.objects.filter(categories__in=[category])
        return render(request, 'blog/latest_posts.html', context)
    
    @route(r'^latest/?$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:2]
        
        return render(request, 'blog/latest_posts.html', context)
    
    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_posts'),
                'lastmod' : (self.last_published_at or self.latest_revision_created_at),
                'priority': 0.9,
            }
        )
        
        return sitemap


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogDetailPage(Page):
    """Parental Blog Detail Page"""
    
    subpage_types = []
    parent_page_types = ['blog.BlogListingPage']
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    
    excerpt = models.CharField(
        max_length=250,
        blank=False,
        null=True
    )
    
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    # tags = ParentalManyToManyField('blog.BlogTag', blank=True)
    
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
            ('quote', blocks.BlockQuote()),
        ],
        null=True,
        blank=True,
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('blog_image'),
        FieldPanel('excerpt'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label=_('Author'), min_num=1, max_num=2),
            ],
            heading=_('Author(s)')
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading=_('Categories')
        ),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('tags', widget=forms.CheckboxSelectMultiple)
        #     ],
        #     heading=_('Tags')
        # ),
        FieldPanel('tags'),
        FieldPanel('content'),
    ]
    
    api_fields = [
        APIField('blog_authors'),
        APIField('categories'),
        # APIField('tags'),
    ]
    
    # Method to delete caches of a piece of code when it has been updated
    def save(self, *args, **kwargs):
        key = make_template_fragment_key('blog_post_preview', [self.id])
        cache.delete(key)
        
        key = make_template_fragment_key('article_post_preview')
        cache.delete(key)
        
        return super().save(*args, **kwargs)


class ArticleBlogPage(BlogDetailPage):
    """A subclass bolg post page for articles"""
    
    template = 'blog/blog_article_page.html'
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Best size for this image 1200px X 800px')
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('intro_image'),
        FieldPanel('blog_image'),
        FieldPanel('excerpt'),
        MultiFieldPanel(
            [
                InlinePanel(
                    'blog_authors',
                    label=_('Author'),
                    min_num=1, max_num=2
                ),
            ],
            heading=_('Author(s)')
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading=_('Categories')
        ),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('tags', widget=forms.CheckboxSelectMultiple)
        #     ],
        #     heading=_('Tags')
        # ),
        FieldPanel('tags'),
        FieldPanel('content'),
    ]


class VideoBlogPage(BlogDetailPage):
    template = 'blog/blog_video_page.html'
    youtube_video_id = models.CharField(max_length=30)
    
    content_panels = Page.content_panels + [
        FieldPanel('blog_image'),
        FieldPanel('excerpt'),
        MultiFieldPanel(
            [
                InlinePanel(
                    'blog_authors',
                    label=_('Author'),
                    min_num=1, max_num=2
                ),
            ],
            heading=_('Author(s)')
        ),
        MultiFieldPanel(
            [
                FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
            ],
            heading=_('Categories')
        ),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('tags', widget=forms.CheckboxSelectMultiple)
        #     ],
        #     heading=_('Tags')
        # ),
        FieldPanel('tags'),
        FieldPanel('youtube_video_id'),
        FieldPanel('content'),
    ]
