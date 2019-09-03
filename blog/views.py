from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from blog.models import Post
from . import models


class Index(ListView):
    queryset = Post.objects.all().order_by('id').reverse()
    template_name = 'blog/index.html'


class NewPost(CreateView):
    model = models.Post
    fields = ['title', 'content', 'publish_date', 'is_draft']
    success_url = reverse_lazy('blog:index')
