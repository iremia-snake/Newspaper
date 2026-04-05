from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from utils import image_cleanup, rename_file
from users.models import Person


def news_image_path(instance, filename):
    return rename_file.uuid_file_path(instance, 'news_images', filename)


class Article(models.Model):
    title = models.CharField('Название', max_length=63)
    #TODO
    # ну либо используй anons, либо удали
    anons = models.CharField('Анонс', max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Картинка к новости')
    content = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации', null=True)
    author = models.ForeignKey(Person, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


@receiver(pre_save, sender=Article)
def delete_old_image_on_update(sender, instance, **kwargs):
    image_cleanup.delete_old_image_on_instance_update(instance, 'image')


@receiver(post_delete, sender=Article)
def del_avatar_on_del(sender, instance, **kwargs):
    image_cleanup.delete_image_on_instance_delete(instance, 'image')
