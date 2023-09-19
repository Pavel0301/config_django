from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from blog.models import Post


class FeedListView(ListView):
    model = Post
    template_name = 'blog/feed_list.html'
    context_object_name = 'feed_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            context['tag'] = tag

        return context


feed_list_view = FeedListView.as_view()


class FeedDetailView(DetailView):
    model = Post
    template_name = 'blog.feed_detail.html'
    context_object_name = 'feed_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['slug'] = slug
        return context


feed_detail_view = FeedDetailView.as_view()



