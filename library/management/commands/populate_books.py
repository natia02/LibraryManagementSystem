import random
from django.core.management.base import BaseCommand
from library.models import Author, Genre, Book
from faker import Faker


class Command(BaseCommand):
    help = 'Populate the database with sample books'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create sample genres
        genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Biography"]
        genre_objects = []
        for genre in genres:
            genre_obj, created = Genre.objects.get_or_create(name=genre)
            genre_objects.append(genre_obj)

        # Create sample authors
        author_objects = []
        for _ in range(100):
            author = Author.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                date_of_birth=faker.date_of_birth()
            )
            author_objects.append(author)

        # Create sample books
        for _ in range(1000):
            book = Book.objects.create(
                title=faker.sentence(nb_words=4),
                author=random.choice(author_objects),
                date_of_issue=faker.date_this_century(),
                quantity=random.randint(1, 20)
            )
            book.genre.set(random.sample(genre_objects, k=random.randint(1, 3)))
            book.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample books.'))
