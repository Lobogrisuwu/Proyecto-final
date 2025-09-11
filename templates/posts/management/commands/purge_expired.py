from django.core.management.base import BaseCommand
from django.utils import timezone
from posts.models import Post

class Command(BaseCommand):
    help = "Borra posts y archivos vencidos"

    def handle(self, *args, **kwargs):
        qs = Post.objects.filter(expires_at__lte=timezone.now())
        count = qs.count()
        for p in qs:
            p.delete()  # dispara signal que intenta borrar imagen S3
        self.stdout.write(self.style.SUCCESS(f"Eliminados {count} posts vencidos"))
