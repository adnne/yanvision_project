from django.db import models
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.search import index
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')

        paginator = Paginator(blogpages,2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts= paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=False)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog information :"),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]


class BlogTagIndexPage(Page):

    def get_context(self, request):

        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

