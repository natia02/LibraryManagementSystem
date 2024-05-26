from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff status'))
    is_customer = models.BooleanField(default=True, verbose_name=_('Customer status'))
    personal_number = models.CharField(max_length=11, unique=True, verbose_name=_('Personal number'))
    birth_date = models.DateField(verbose_name=_('Birth Date'), null=True, blank=True)

    def __str__(self):
        return self.username + ' ' + self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Genre Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    date_of_issue = models.DateField(null=True, blank=True, verbose_name=_('Date of issue'))
    quantity = models.PositiveIntegerField(default=0, verbose_name=_('Quantity'))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    genre = models.ManyToManyField(Genre, verbose_name=_('Genres'), related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')


class BookBorrowingHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowing_history', verbose_name=_('Book'))
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Borrower'))
    borrowing_date = models.DateField(default=timezone.now, verbose_name=_('Borrowing Date'))
    return_date = models.DateField(null=True, blank=True, verbose_name=_('Return Date'))

    def __str__(self):
        return f"{self.book.title} - Borrowed by {self.borrower.username}"

    class Meta:
        verbose_name = _('Book Borrowing History')
        verbose_name_plural = _('Book Borrowing Histories')


class BookReservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('User'))
    reservation_date = models.DateField(default=date.today, verbose_name=_('Reservation Date'))

    class Meta:
        verbose_name = _('Book Reservation')
        verbose_name_plural = _('Book Reservations')
