from django.utils import timezone
from rest_framework import serializers
from rest_framework.request import Request

from library.models import (CustomUser, Book,
                            Author, Genre,
                            BookBorrowingHistory, BookReservation)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'email', 'personal_number', 'birth_date', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        @staticmethod
        def create(self, validated_data):
            validated_data['is_staff'] = False
            validated_data['is_superuser'] = False
            user = CustomUser.objects.create_user(**validated_data)
            return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author,
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookBorrowingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrowingHistory
        fields = ['borrower', 'borrowing_date', 'return_date']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.resolver_match and request.resolver_match.url_name == 'book-detail':
            data['times_borrowed'] = instance.borrowing_history.count()
            data['available_copies'] = instance.quantity - instance.borrowing_history.filter(
                return_date__isnull=True).count()
            data['checked_out_copies'] = instance.borrowing_history.filter(return_date__isnull=True).count()
            data['borrowing_history'] = BookBorrowingHistorySerializer(instance.borrowing_history.all(), many=True).data

        return data

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        genres_data = validated_data.pop('genre', None)

        if author_data is not None:
            author = author_data
        else:
            author = None

        if genres_data is not None:
            genres = [Genre.objects.get_or_create(pk=genre_data.pk)[0] for genre_data in genres_data]
        else:
            genres = []

        book = Book.objects.create(
            title=validated_data.get('title'),
            date_of_issue=validated_data.get('date_of_issue'),
            quantity=validated_data.get('quantity'),
            author=author,
        )

        book.genre.set(genres)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        genres_data = validated_data.pop('genre', None)

        if author_data is not None:
            author = author_data
        else:
            author = instance.author

        if genres_data is not None:
            genres = [Genre.objects.get_or_create(pk=genre_data.pk)[0] for genre_data in genres_data]
        else:
            genres = instance.genre.all()

        instance.title = validated_data.get('title', instance.title)
        instance.date_of_issue = validated_data.get('date_of_issue', instance.date_of_issue)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.author = author
        instance.save()
        instance.genre.set(genres)
        return instance

    @staticmethod
    def delete(self, instance):
        instance.delete()


class BookReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReservation
        fields = '__all__'
        read_only_fields = ['user']

