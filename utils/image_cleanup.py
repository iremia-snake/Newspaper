import os


def delete_old_image_on_instance_update(instance, image_field_name):
    """
    Удаляет старое изображение при обновлении
    """
    if not instance.pk:  # Новая запись, нечего удалять
        return None

    try:
        model_class = instance.__class__
        old_instance = model_class.objects.get(pk=instance.pk)
        old_image_field = getattr(old_instance, image_field_name)
        new_image_field = getattr(instance, image_field_name)

        if old_image_field and old_image_field != new_image_field:
            if old_image_field.name and os.path.isfile(old_image_field.path):
                os.remove(old_image_field.path)
                print(f"Удален старый файл: {old_image_field.path}")

    except (ValueError, OSError) as e:
        # Файл уже удален или недоступен
        print(f"Не удалось удалить файл: {e}")
        pass


def delete_image_on_instance_delete(instance, image_field_name):
    """
    Удаляет изображение при удалении записи
    """
    # Получаем поле с изображением
    image_field = getattr(instance, image_field_name)

    if image_field:
        try:
            if image_field.name and os.path.isfile(image_field.path):
                os.remove(image_field.path)
                print(f"Удален файл при удалении записи: {image_field.path}")
        except (ValueError, OSError) as e:
            print(f"Не удалось удалить файл при удалении: {e}")
            pass
