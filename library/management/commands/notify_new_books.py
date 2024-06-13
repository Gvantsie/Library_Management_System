import smtplib
from email.mime.text import MIMEText
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

from library.models.book import Book


class Command(BaseCommand):
    help = 'Send an email notification to all authorized users when a new book is added.'

    def handle(self, *args, **kwargs):
        new_books = Book.objects.filter(notified=False)
        if not new_books:
            self.stdout.write(self.style.SUCCESS('No new books to notify.'))
            return

        User = get_user_model()  # Use the custom user model
        users = User.objects.filter(is_active=True)
        if not users:
            self.stdout.write(self.style.SUCCESS('No active users to notify.'))
            return

        for book in new_books:
            for user in users:
                self.send_email(user.email, book)
            book.notified = True
            book.save()

        self.stdout.write(self.style.SUCCESS('Emails sent to all users about new books.'))

    def send_email(self, to_email, book):
        subject = 'New Book Added: {}'.format(book.title)
        body = ('We are happy to inform you that a new book titled "{}" by {} has been added to our library. '
                'Visit us to explore plenty of interesting collection!').format(book.title, book.author)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = to_email

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [to_email], msg.as_string())
            server.quit()
            self.stdout.write(self.style.SUCCESS('Email sent to {}'.format(to_email)))
        except Exception as exception:
            self.stdout.write(self.style.ERROR('Failed to send email to {}: {}'.format(to_email, exception)))
