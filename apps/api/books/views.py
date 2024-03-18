from rest_framework import viewsets, status, generics, views
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.core.paginator import Paginator
from rest_framework.response import Response
from .models import Book, Author, Bookshelf, Format, Language, Subject
from .serializers import BooksSerializer

import os


class BookViewSet(viewsets.ModelViewSet):
    """
    View set for handling CRUD operations on categories.

    This view set provides endpoints for listing, creating, retrieving, updating, and deleting categories.

    Attributes:
        queryset (QuerySet): The queryset containing all categories.
        serializer_class (Serializer): The serializer class used for serializing/deserializing categories.
    """
    queryset = Book.objects.all()[:30]
    serializer_class = BooksSerializer
    

# class BooksAPIView(generics.ListAPIView):
#     queryset = Book.objects.order_by('-download_count')
#     serializer_class = BooksSerializer
#     pagination_class = PageNumberPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = {
#         'gutenberg_id': ['exact'],
#         'language__code': ['exact'],
#         'title': ['icontains'],
#     }
class BooksAPIView(views.APIView):
    def get(self, request):
        # Retrieve filter criteria from request query parameters
        gutenberg_id = request.query_params.get('gutenberg_id')
        language = request.query_params.get('language')
        mime_type = request.query_params.get('mime_type')
        topic = request.query_params.get('topic')
        author = request.query_params.get('author')
        title = request.query_params.get('title')

        # Filter books based on the provided criteria
        books = Book.objects.all()
        if gutenberg_id:
            books = books.filter(gutenberg_id=gutenberg_id)
        if language:
            books = books.filter(language__code=language)
        if mime_type:
            books = books.filter(format__mime_type=mime_type)
        if topic:
            books = books.filter(booksubject__subject__name__icontains=topic)
        if author:
            books = books.filter(bookauthor__author__name__icontains=author)
        if title:
            books = books.filter(title__icontains=title)

        # # Annotate each book with download count
        # books = books.annotate(download_count=Count('format'))

        # Sort books by download count in descending order
        books = books.order_by('-download_count')

        # Paginate the queryset
        paginator = Paginator(books, 20)
        page_number = request.query_params.get('page', 1)
        page = paginator.get_page(page_number)

        # Serialize the paginated queryset
        serializer = BooksSerializer(page, many=True)

        # Return the paginated response
        return Response({
            'total_books': paginator.count,
            'books': serializer.data
        })