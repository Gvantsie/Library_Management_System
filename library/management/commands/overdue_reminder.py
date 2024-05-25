from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.conf import settings
from library.models.reservation import Reservation


# Command to send email reminders for overdue book reservations
class Command(BaseCommand):
    help = 'Sends email reminders for overdue book reservations.'

    def handle(self, *args, **options):
        overdue_reservations = Reservation.objects.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        )

        emails = []
        for reservation in overdue_reservations:
            subject = f'Overdue Book Reminder: {reservation.book.title}'
            message = f'Dear {reservation.user.get_full_name()},\n\n'
            message += f'This is a friendly reminder that the book "{reservation.book.title}" is overdue for return.\n'
            message += 'Please return the book as soon as possible to avoid any penalties.\n\n'
            message += 'Thank you for your cooperation.'

            from_email = settings.EMAIL_HOST_USER
            to_email = reservation.user.email
            emails.append((subject, message, from_email, [to_email]))

        send_mass_mail(tuple(emails))
        self.stdout.write(self.style.SUCCESS('Overdue reminders sent successfully.'))