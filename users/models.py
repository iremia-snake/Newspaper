from django.contrib.auth.models import AbstractUser
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from utils import image_cleanup, rename_file


def user_avatar_path(instance, filename):
    return rename_file.uuid_file_path(instance, 'avatars', filename)


class Person(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='О себе')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')

    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


# обновление записи
@receiver(pre_save, sender=Person)
def del_avatar(sender, instance, **kwars):
    image_cleanup.delete_old_image_on_instance_update(instance, 'avatar')


# удаление записи
@receiver(post_delete, sender=Person)
def del_avatar_on_del(sender, instance, **kwargs):
    image_cleanup.delete_image_on_instance_delete(instance, 'avatar')
