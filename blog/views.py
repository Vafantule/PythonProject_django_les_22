from django import forms
from .models import BlogPost
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class BlogPostForm(forms.ModelForm):
    """
    Форма создания и редактирования записей блога.
    """
    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published"]


class BlogListView(ListView):
    """
    Контроллер отображения списка записей блогов.
    """
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"


class BlogDetailView(DetailView):
    """
    Контроллер отображения одной записи блога.
    """
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"
    pk_url_kwarg = "pk"


class BlogCreateView(CreateView):
    """
    Контроллер создания записи блога.
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    """
    Контроллер обновления записи блога.
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")
    pk_url_kwarg = "pk"
    context_object_name = "blog"


class BlogDeleteView(DeleteView):
    """
    Контроллер удаления записи блога.
    """
    model = BlogPost
    template_name = "blog/blog_delete_confirm.html"
    success_url = reverse_lazy("blog:blog_list")
    pk_url_kwarg = "pk"
    context_object_name = "blog"
