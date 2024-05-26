from rest_framework import generics, filters, viewsets, status, views
from library.serializers import UserRegistrationSerializer, BookSerializer, BookReservationSerializer
from library.models import CustomUser, Book, BookReservation, BookBorrowingHistory
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(serializer.data)


class CustomLoginView(TokenObtainPairView, views.APIView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=204)
        except Exception as e:
            return Response(str(e), status=400)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'genre', 'title']
    search_fields = ['title']


class BookReservationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = BookReservationSerializer(data=request.data)
        if serializer.is_valid():
            book_id = request.data.get('book')
            book = get_object_or_404(Book, pk=book_id)
            if book.quantity > 0:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'The book is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        reservation = get_object_or_404(BookReservation, pk=pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        reservations = BookReservation.objects.all()
        serializer = BookReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        reservation = get_object_or_404(BookReservation, pk=pk)
        serializer = BookReservationSerializer(reservation)
        return Response(serializer.data)

    def get(self, request):
        serializer = BookReservationSerializer()
        return Response(serializer.data)
