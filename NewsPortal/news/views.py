from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category, Subscriber


class PostList(ListView):
    model = Post
    ordering = '-date_post'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsList(PostList):
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(category_type='NW')
        return queryset


class ArticleList(PostList):
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(category_type='AR')
        return queryset
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post_detail'


class AuthorList(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'news/authors.html'


class SearchList(ListView):
    model = Post
    ordering = '-date_post'
    context_object_name = 'search'
    template_name = 'news/search_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-date_post')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#
#     message = "Вы успешно подписались на рассылку публикаций категории"
#     return render(request, 'news/subscribe.html', {'category': category, 'message': message})

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, subscription=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                subscription=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                subscription=OuterRef('pk'),
            )
        )
    ).order_by('name_cat')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )