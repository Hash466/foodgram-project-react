from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True,)
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name="Подписчик",
                             on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User, verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"
