from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, Author, Genre, CustomUser, BookBorrowingHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'date_of_issue', 'quantity')
    list_filter = ('author', 'genre', 'date_of_issue', 'quantity')
    search_fields = ('title', 'author__name')

    @admin.display(description='Genre')
    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    @admin.display(description='Times Borrowed')
    def times_borrowed(self, obj):
        return obj.borrowing_history.count()

    @admin.display(description='Available Copies')
    def available_copies(self, obj):
        return obj.quantity - obj.borrowing_history.filter(return_date__isnull=True).count()

    @admin.display(description='Checked Out Copies')
    def checked_out_copies(self, obj):
        return obj.borrowing_history.filter(return_date__isnull=True).count()

    @admin.display(description='Borrowing History')
    def borrowing_history(self, obj):
        borrowings = obj.borrowing_history.all()
        if borrowings:
            return "\n".join([f"{b.borrower.username} - {b.borrowing_date} to {b.return_date}" for b in borrowings])
        else:
            return "No borrowing history yet."

    readonly_fields = ('times_borrowed', 'available_copies', 'checked_out_copies', 'borrowing_history')

    fieldsets = (
        (None, {'fields': ('title', 'author', 'genre', 'date_of_issue', 'quantity')}),
        ('Borrowing Information', {'fields': ('times_borrowed', 'available_copies',
                                              'checked_out_copies', 'borrowing_history')})
    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'personal_number', 'is_staff', 'is_customer')
    list_filter = ('is_staff', 'is_customer', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'personal_number')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_date')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_customer', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('personal_number',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'email', 'birth_date', 'personal_number', 'password1',
                'password2',
                'is_staff', 'is_customer'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_customer'
        return ()
