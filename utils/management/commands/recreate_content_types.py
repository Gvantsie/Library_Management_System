from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Recreate content types for all installed apps'

    def handle(self, *args, **options):
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                ContentType.objects.get_or_create(
                    app_label=app_config.label,
                    model=model._meta.model_name
                )
        self.stdout.write(self.style.SUCCESS('Successfully recreated content types'))
