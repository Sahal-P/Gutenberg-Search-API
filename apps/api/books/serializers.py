from rest_framework import serializers
from .models import Book, Author, Bookshelf, Format, Language, Subject

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']
        
class BooksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    This serializer is used to serialize Book instances into JSON representation.
    """
    id = serializers.IntegerField(source='gutenberg_id', read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    formats = FormatSerializer(source='format_set', many=True)


    class Meta:
        model = Book
        fields = ['id' ,'title', 'download_count', 'media_type', 'authors', 'bookshelves', 'languages', 'subjects', 'formats']
