from typing import Any

from django import forms
from .models import BlogPost
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden


class BlogManagePermissionMixin(UserPassesTestMixin):
    """
    Миксин только для контент-менеджеров.
    """
    def is_content_manager(self) -> bool:
        user = self.request.user
        return user.is_authenticated and any(
            group.name == "Контент-менеджер" for group in user.groups.all()
        )

    def test_func(self) -> bool:
        return self.is_content_manager()

    def handle_no_permission(self):
        return HttpResponseForbidden("Доступ запрещён. Только для контент-менеджеров.")


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

    def get_queryset(self):
        """
        Возвращает только опубликованные записи.
        """
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """
    Контроллер отображения одной записи блога.
    """
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"
    pk_url_kwarg = "pk"

    def get_object(self, queryset=None) -> BlogPost:
        """
        Обновление счетчика просмотров.
        """
        blog = super(). get_object(queryset)
        blog.views_count += 1
        blog.save(update_fields=["views_count"])
        return blog


class BlogCreateView(LoginRequiredMixin, BlogManagePermissionMixin, CreateView):
    """
    Контроллер создания записи блога.
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blog_form.html"

    def form_valid(self, form: BlogPostForm) -> Any:
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


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

    def get_success_url(self) -> str:
        """
        Возвращает на страницу после редактирования записи.
        """
        return reverse("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    """
    Контроллер удаления записи блога.
    """
    model = BlogPost
    template_name = "blog/blog_delete_confirm.html"
    success_url = reverse_lazy("blog:blog_list")
    pk_url_kwarg = "pk"
    context_object_name = "blog"
