from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Post


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def clear_post_cache(sender, **kwargs):
    cache.clear()