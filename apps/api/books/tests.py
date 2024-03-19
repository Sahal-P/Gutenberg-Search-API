from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author, Bookshelf, Language, Subject, Format

class BooksAPITestCase(APITestCase):
    """
    Test case for the Books API view.
    """
    def setUp(self):
        """
        Set up test data.
        """
        author1 = Author.objects.create(name="Jane Austen", birth_year=1775, death_year=1817)
        author2 = Author.objects.create(name="Mark Twain", birth_year=1835, death_year=1910)

        bookshelf1 = Bookshelf.objects.create(name="Best Books Ever Listings")
        bookshelf2 = Bookshelf.objects.create(name="Harvard Classics")

        language1 = Language.objects.create(code="en")
        language2 = Language.objects.create(code="fr")

        subject1 = Subject.objects.create(name="Domestic fiction")
        subject2 = Subject.objects.create(name="Love stories")
        subject3 = Subject.objects.create(name="Young women -- Fiction")
        subject4 = Subject.objects.create(name="England -- Fiction")
        subject5 = Subject.objects.create(name="Sisters -- Fiction")
        subject6 = Subject.objects.create(name="Social classes -- Fiction")
        subject7 = Subject.objects.create(name="Courtship -- Fiction")

        book1 = Book.objects.create(title="Pride and Prejudice", download_count=44776, gutenberg_id=1342, media_type="Text")
        book1.authors.add(author1)
        book1.bookshelves.add(bookshelf1, bookshelf2)
        book1.languages.add(language1)
        book1.subjects.add(subject1, subject2, subject3, subject4, subject5, subject6, subject7)

        book2 = Book.objects.create(title="Adventures of Huckleberry Finn", download_count=30000, gutenberg_id=76, media_type="Text")
        book2.authors.add(author2)
        book2.bookshelves.add(bookshelf1)
        book2.languages.add(language2)
        book2.subjects.add(subject2, subject6)

        Format.objects.create(mime_type="text/html; charset=utf-8", url="http://www.gutenberg.org/files/1342/1342-h.zip", book=book1)
        Format.objects.create(mime_type="application/epub+zip", url="http://www.gutenberg.org/ebooks/1342.epub.images", book=book1)
        Format.objects.create(mime_type="text/plain; charset=utf-8", url="http://www.gutenberg.org/files/1342/1342-0.txt", book=book1)

        Format.objects.create(mime_type="text/html; charset=utf-8", url="http://www.gutenberg.org/files/76/76-h.zip", book=book2)
        Format.objects.create(mime_type="application/epub+zip", url="http://www.gutenberg.org/ebooks/76.epub.images", book=book2)
        Format.objects.create(mime_type="text/plain; charset=utf-8", url="http://www.gutenberg.org/files/76/76-0.txt", book=book2)

    def test_books_api_view(self):
        url = reverse("books-api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_books_api_with_topic_filter(self):
        url = reverse("books-api")
        response = self.client.get(url, {"topic": "fiction"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5) 
    
    def test_books_api_with_multiple_languages(self):
        url = reverse("books-api")
        response = self.client.get(url, {"languages": "en, fr"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2) 
        

    def test_books_api_with_invalid_topic(self):
        url = reverse("books-api")
        response = self.client.get(url, {"topic": "nonexistent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)