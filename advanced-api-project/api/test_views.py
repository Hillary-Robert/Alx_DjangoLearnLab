from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Tests for the Book API endpoints.

    What we test here:
    - CRUD operations for the Book model:
        * List books (GET /api/books/)
        * Create book (POST /api/books/)
        * Retrieve single book (GET /api/books/<id>/)
        * Update book (PUT/PATCH /api/books/<id>/)
        * Delete book (DELETE /api/books/<id>/)
    - Filtering, searching and ordering on the book list endpoint.
    - Basic authentication / permission behavior:
        * Unauthenticated requests are rejected.
        * Authenticated requests are allowed.
    """

    def setUp(self):
        """
        setUp runs before EACH test method.

        Here we:
        - Create a test user.
        - Log in the user so requests are authenticated.
        - Create some authors and books to use in tests.
        """
        # Create a user for authentication
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        # Log in the user (uses Django's session auth)
        self.client.login(username="testuser", password="testpass123")

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books with different titles, years and authors
        self.book1 = Book.objects.create(
            title="Alpha Book",
            publication_year=2000,
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title="Beta Book",
            publication_year=2010,
            author=self.author1,
        )
        self.book3 = Book.objects.create(
            title="Gamma Stories",
            publication_year=2005,
            author=self.author2,
        )

        # URL helpers
        # These names must match the names used in api/urls.py
        self.list_url = reverse("book-list")

    def _detail_url(self, pk: int) -> str:
        """Helper to get the detail URL for a specific book."""
        return reverse("book-detail", args=[pk])

    # ------------------------------------------------------------------
    # AUTH / PERMISSIONS
    # ------------------------------------------------------------------

    def test_book_list_requires_authentication(self):
        """
        If default DRF permissions are set to IsAuthenticated,
        unauthenticated requests should NOT be allowed.

        This test:
        - Logs the user out.
        - Calls GET /api/books/
        - Expects a 401 or 403 status code (depending on auth backend).
        """
        self.client.logout()  # ensure no user is logged in

        response = self.client.get(self.list_url)

        # Depending on your settings you may get 401 or 403.
        # We accept either here.
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    # ------------------------------------------------------------------
    # CRUD TESTS
    # ------------------------------------------------------------------

    def test_list_books_authenticated(self):
        """
        Authenticated user should be able to list books.

        - Expect HTTP 200.
        - Expect the correct number of books.
        """
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response should be a list of 3 books
        self.assertEqual(len(response.data), 3)

    def test_create_book(self):
        """
        Authenticated user can create a new book via POST /api/books/.

        - Send valid data.
        - Expect HTTP 201 CREATED.
        - Check that the book exists in the database.
        """
        data = {
            "title": "New Created Book",
            "publication_year": 2024,
            "author": self.author1.id,
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

        # Check last created book
        new_book = Book.objects.get(title="New Created Book")
        self.assertEqual(new_book.publication_year, 2024)
        self.assertEqual(new_book.author, self.author1)

    def test_retrieve_single_book(self):
        """
        Authenticated user can retrieve a single book by id.

        - GET /api/books/<id>/
        - Expect HTTP 200.
        - Check returned fields.
        """
        url = self._detail_url(self.book1.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.id)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_update_book(self):
        """
        Authenticated user can update a book via PUT.

        - Change the title and publication_year.
        - Expect HTTP 200.
        - Confirm the changes were saved.
        """
        url = self._detail_url(self.book1.id)
        data = {
            "title": "Updated Alpha Book",
            "publication_year": 1999,
            "author": self.author1.id,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha Book")
        self.assertEqual(self.book1.publication_year, 1999)

    def test_partial_update_book(self):
        """
        Authenticated user can partially update a book via PATCH.

        - Only change the title.
        - Expect HTTP 200.
        - Confirm other fields stay the same.
        """
        url = self._detail_url(self.book2.id)
        data = {
            "title": "Partially Updated Title",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Partially Updated Title")
        self.assertEqual(self.book2.publication_year, 2010)

    def test_delete_book(self):
        """
        Authenticated user can delete a book via DELETE.

        - Expect HTTP 204 NO CONTENT.
        - Confirm the book is removed from the database.
        """
        url = self._detail_url(self.book3.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())

    # ------------------------------------------------------------------
    # FILTERING, SEARCHING, ORDERING
    # ------------------------------------------------------------------

    def test_filter_books_by_publication_year(self):
        """
        Test filtering using ?publication_year=2010

        Expect:
        - Only the book with publication_year=2010 is returned.
        """
        response = self.client.get(self.list_url, {"publication_year": 2010})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Beta Book")

    def test_filter_books_by_author_name(self):
        """
        Test filtering using ?author__name=Author%20One

        Expect:
        - Only books written by 'Author One' are returned.
        """
        response = self.client.get(self.list_url, {"author__name": "Author One"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Author One has book1 and book2
        self.assertEqual(len(response.data), 2)

        returned_titles = sorted([book["title"] for book in response.data])
        self.assertEqual(returned_titles, ["Alpha Book", "Beta Book"])

    def test_search_books_by_title(self):
        """
        Test search using ?search=Gamma

        Expect:
        - Only 'Gamma Stories' is returned.
        """
        response = self.client.get(self.list_url, {"search": "Gamma"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Gamma Stories")

    def test_search_books_by_author_name(self):
        """
        Test search using ?search=Author%20Two

        Expect:
        - All books written by 'Author Two' are returned.
        """
        response = self.client.get(self.list_url, {"search": "Author Two"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], self.author2.id)

    def test_order_books_by_title_ascending(self):
        """
        Test ordering using ?ordering=title

        Expect:
        - Books returned in alphabetical order of title.
        """
        response = self.client.get(self.list_url, {"ordering": "title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["Alpha Book", "Beta Book", "Gamma Stories"])

    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering using ?ordering=-publication_year

        Expect:
        - Books returned from newest to oldest.
        """
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, [2010, 2005, 2000])
