from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name='profile',
        verbose_name='Пользователь',
    )
    registration_date = models.DateField(auto_now_add=True, null=False, verbose_name='Дата регистрации')

    def __str__(self):
        return f'Профиль пользователя {self.user}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Blog(models.Model):
    """Модель блога пользователя"""
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name='blog',
        verbose_name='Пользователь',
    )

    def __str__(self):
        return f'Блог пользователя {self.user}'

    def get_absolute_url(self):
        return reverse('user_blog', args=[self.user.username])

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


class BlogPost(models.Model):
    """Модель публикации в блоге"""
    blog = models.ForeignKey(
        to=Blog,
        on_delete=models.CASCADE,
        null=False,
        related_name='blog_posts',
        verbose_name='Блог',
    )
    text = models.TextField(null=False, verbose_name='Текст публикации')
    pub_date = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Дата публикации')
    delete_date = models.DateTimeField(null=True, default=None, verbose_name='Дата удаления')

    def __str__(self):
        return f'Публикация пользователя {self.blog.user}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )
