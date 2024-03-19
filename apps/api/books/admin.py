from django.contrib import admin
from .models import Book, Author, Bookshelf, Format, Language, Subject

admin.site.register(Book)
admin.site.register(Bookshelf)
admin.site.register(Format)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Subject)