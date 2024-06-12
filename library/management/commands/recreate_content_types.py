from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        help = 'Recreate content types for all installed apps'

        # Check if any ContentType objects exist
        if ContentType.objects.exists():
            last_contenttype = ContentType.objects.latest('id')
            next_id = last_contenttype.id + 1
        else:
            next_id = 1

        # Recreate content types for all installed apps
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                content_type, created = ContentType.objects.get_or_create(
                    app_label=app_config.label,
                    model=model._meta.model_name,
                    defaults={'id': next_id}
                )
                if created:
                    next_id += 1

        self.stdout.write(self.style.SUCCESS('Successfully recreated content types'))
