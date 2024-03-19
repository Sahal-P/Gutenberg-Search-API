from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Bookshelf(models.Model):
    name = models.CharField(max_length=64)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Language(models.Model):
    code = models.CharField(max_length=4)
    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]

class Subject(models.Model):
    name = models.CharField(max_length=256)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

class Book(models.Model):
    """
    The title of the book.

    This field stores the title of the book. It can be null and blank.
    """
    title = models.CharField(max_length=1024, null=True, blank=True)
    
    """
    The number of times the book has been downloaded.

    This field stores the count of how many times the book has been downloaded. 
    It defaults to 0 if not provided.
    
    """
    download_count = models.IntegerField(default=0)
    
    """
    The unique identifier of the book in the Gutenberg database.

    This field stores the unique identifier of the book as assigned by the Gutenberg project.
    """
    gutenberg_id = models.IntegerField()
    
    """
    The media type of the book.

    This field stores the media type of the book, such as text, image, or audio.
    """
    media_type = models.CharField(max_length=16)
    
    """
    The authors of the book.

    This field represents the authors of the book. It is a many-to-many relationship with the Author model.
    """
    authors = models.ManyToManyField(Author)
    
    """
    The bookshelves where the book is categorized.

    This field represents the bookshelves where the book is categorized.
    It is a many-to-many relationship with the Bookshelf model.
    """
    bookshelves = models.ManyToManyField(Bookshelf)
    
    """
    The languages in which the book is available.

    This field represents the languages in which the book is available.
    It is a many-to-many relationship with the Language model.
    """
    languages = models.ManyToManyField(Language)
    
    """
    The subjects or genres of the book.

    This field represents the subjects or genres of the book.
    It is a many-to-many relationship with the Subject model.
    """
    subjects = models.ManyToManyField(Subject)
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
    
class Format(models.Model):
    """
    Model for storing book format details.

    Fields:
    - mime_type: The MIME type of the book format.
    - url: The URL where the book format can be accessed.
    - book: Foreign key representing the associated book.
    """
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    