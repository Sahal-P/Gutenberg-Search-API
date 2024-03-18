from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)





# class BookAuthor(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "books_book_authors"


class Bookshelf(models.Model):
    name = models.CharField(max_length=64)


# class BookBookshelf(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "books_book_bookshelves"





class Language(models.Model):
    code = models.CharField(max_length=4)


# class BookLanguage(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "books_book_languages"


class Subject(models.Model):
    name = models.CharField(max_length=256)


# class BookSubject(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "books_book_subjects"

class Book(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=True)
    download_count = models.IntegerField(default=0)
    gutenberg_id = models.IntegerField()
    media_type = models.CharField(max_length=16)
    authors = models.ManyToManyField(Author)
    bookshelves = models.ManyToManyField(Bookshelf)
    languages = models.ManyToManyField(Language)
    subjects = models.ManyToManyField(Subject)
    
    
class Format(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    