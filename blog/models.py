from django.db import models


class BlogPost(models.Model):
    """
    Модель для ведения блога.
    """
    title: str = models.CharField(max_length=255, verbose_name="Заголовок")
    content: str = models.TextField(verbose_name="Содержимое")
    preview: str = models.ImageField(upload_to="blog_previews/", blank=True, null=True, verbose_name="Превью")
    created_at: "datetime" = models.DateTimeField(auto_now_add=True, verbose_name="Дата создание")
    update_at: "datetime" = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_published: bool = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count: int = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Запись блога"
        verbose_name_plural = "Записи блогов"

    def __str__(self):
        """
        Строковое представление записи блога.
        """
        return self.title
