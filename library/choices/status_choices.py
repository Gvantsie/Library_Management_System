from model_utils import Choices

STATUS_CHOICES = Choices(
    ('available', 'ხელმისაწვდომი'),
    ('not_available', 'გატანილი'),
    ('reserved', 'დაჯავშნილი'),
    ('lost', 'დაკარგული'),
)
