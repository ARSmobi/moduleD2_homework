from django.shortcuts import redirect
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, TemplateView)
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('id')
    paginate_by = 10
    ordering = ['-dateCreation']
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['choices'] = Post.CATEGORY_CHOICES
        context['form'] = PostForm()
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['author'] = self.request.user.username
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.username
        return context


class AddPost(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    success_url = '/news/search/'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()

        # html_content = render_to_string(
        #     'post_created.html',
        #     {
        #         'post': post
        #     }
        # )
        #
        # msg = EmailMultiAlternatives(
        #     subject=f'{post.title} | {post.dateCreation}',
        #     body=post.text,
        #     from_email='arsmobi.2@gmail.com',
        #     to=['ver.kag@yandex.ru', 'arsmobi@mail.ru'],
        # )
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.username
        return context


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.username
        return context


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:posts')
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user.username
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = '/accounts/logout/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required
def upgrade_to_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/search/')
