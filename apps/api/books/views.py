from rest_framework import viewsets, status, generics, views
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Book
from .serializers import BooksSerializer
from django.shortcuts import get_object_or_404

def parse_comma_separated_param(param_string):
    """
    Parse comma-separated query parameter string into a list of values,
    stripping leading and trailing whitespace from each value.
    """
    return [value.strip() for value in param_string.split(",")] if param_string else []


class BooksAPIView(views.APIView):
    """
    API view for fetching books with various filters and pagination.

    This view handles GET requests to fetch books based on query parameters like title,
    author, languages, MIME type, and topics. It also supports pagination.

    """

    pagination_class = PageNumberPagination

    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle GET requests to fetch books.

        This method retrieves books based on query parameters such as title, author,
        languages, MIME type, and topics. It returns paginated results.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: A paginated response containing the serialized books data.
        """
        params = self.process_request(request)

        filter_args = {}
        print(params)
        queryset = Book.objects.prefetch_related(
            "authors", "bookshelves", "languages", "subjects"
        )
        if params['gutenberg_id']:
            book = get_object_or_404(Book, gutenberg_id=params["gutenberg_id"])
            queryset = queryset.filter(pk=book.pk)
        else:
            if params['title']:
                filter_args["title__icontains"] = params['title']
            if params['author']:
                filter_args["authors__name__icontains"] = params['author']
            if params['languages']:
                filter_args["languages__code__in"] = params['languages']
            if params['mime_type']:
                filter_args["format__mime_type"] = params['mime_type']
            if params['topics']:
                topic_filter = Q()
                for topic in params['topics']:
                    topic_filter |= (Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic))
                queryset = Book.objects.prefetch_related(
                    "authors", "bookshelves", "languages", "subjects"
                ).filter(topic_filter).order_by("-download_count")

                return self.paginate(queryset, request)

            queryset = (
                    Book.objects.prefetch_related(
                        "authors", "bookshelves", "languages", "subjects"
                    )
                    .filter(**filter_args)
                    .order_by("-download_count")
                )

        return self.paginate(queryset=queryset, request=request)

    def process_request(self, request: Request) -> dict:
        """
        Process the incoming request and extract query parameters.
        """
        query_params = {
            "gutenberg_id": request.query_params.get("gutenberg_id"),
            "title": request.query_params.get("title", ""),
            "author": request.query_params.get("author", ""),
            "languages": parse_comma_separated_param(request.query_params.get("languages", [])),
            "mime_type": request.query_params.get("mime_type", ""),
            "topics": parse_comma_separated_param(request.query_params.get("topic", "")),
        }
        return query_params

    def paginate(self, queryset, request):
        """
        Paginate the queryset and return paginated response.

        Args:
            queryset: The queryset to paginate.
            request: The incoming HTTP request.

        Returns:
            Response: A paginated response containing the serialized queryset data.
        """
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = BooksSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
