from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import BookReservation


class Command(BaseCommand):
    help = 'Remove expired book reservations'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_reservations = BookReservation.objects.filter(reservation_date__lt=now - timezone.timedelta(days=1))
        count = expired_reservations.count()
        expired_reservations.delete()
        self.stdout.write(f'Successfully removed {count} expired reservations.')
