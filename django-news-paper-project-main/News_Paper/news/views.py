from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from .models import Post
from django.urls import reverse_lazy

class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-created_at']
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

class NewsSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        date = self.request.GET.get('date_after')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__user__username__icontains=author)
        if date:
            queryset = queryset.filter(created_at__date__gte=date)

        return queryset


class NewsCreate(CreateView):
    model = Post
    template_name = 'news/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'NW'
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    model = Post
    template_name = 'news/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(NewsCreate):
    def form_valid(self, form):
        form.instance.post_type = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class ArticleUpdate(NewsUpdate):
    pass

class ArticleDelete(NewsDelete):
    pass
