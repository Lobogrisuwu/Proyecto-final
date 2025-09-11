# posts/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

def default_expiry():
    return timezone.now() + timedelta(minutes=60)

class Post(models.Model):
    # Dueño “temporal”
    owner_token = models.CharField(max_length=64, db_index=True)    # un UUID que guardamos en sesión
    owner_name  = models.CharField(max_length=30)                   # el nombre que escribió el usuario

    # Contenido
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=2200, blank=True)

    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry, db_index=True)

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"{self.owner_name}: {self.caption[:30]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    owner_token = models.CharField(max_length=64, db_index=True)
    owner_name  = models.CharField(max_length=30)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    owner_token = models.CharField(max_length=64, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'owner_token')

class Follow(models.Model):
    # Ya no usamos seguir/seguidores; la dejamos por compatibilidad si la referenciabas
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

# --- Borrar el archivo en S3 cuando se borra un Post ---
@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    try:
        if instance.image and instance.image.storage.exists(instance.image.name):
            instance.image.delete(save=False)
    except Exception:
        # Evita romper la transacción si S3 falla; el purge periódico volverá a intentar
        pass
