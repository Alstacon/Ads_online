from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    image = models.ImageField(upload_to='images/', default=None, null=True)
    title = models.CharField(max_length=150)
    price = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['created_at']

    @property
    def author_first_name(self):
        return self.author.first_name if self.author else None

    @property
    def author_last_name(self):
        return self.author.last_name if self.author else None

    @property
    def phone(self):
        return self.author.phone if self.author else None

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    @property
    def author_first_name(self):
        return self.author.first_name if self.author else None

    @property
    def author_last_name(self):
        return self.author.last_name if self.author else None

    @property
    def author_image(self):
        return self.author.image if self.author else None

