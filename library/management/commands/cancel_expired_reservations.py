from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from library.models.reservation import Reservation
from library.models.book import Book


class Command(BaseCommand):
    help = 'Cancel expired book reservations'

    def handle(self, *args, **options):
        expired_reservations = Reservation.objects.filter(
            status='reserved',
            reserved_at__lte=timezone.now() - timedelta(days=1)
        )
        for reservation in expired_reservations:
            reservation.status = 'canceled'
            reservation.book.copies_available += 1
            reservation.book.save()
            reservation.save()
        self.stdout.write(self.style.SUCCESS('Successfully canceled expired reservations'))

# when production is running, its better to use cron jobs to run this command periodically.
