## Permissions and Groups Setup (Bookshelf App)

This project defines custom permissions on the `Book` model in `bookshelf/models.py`:

- `can_view` – Can view book list or details.
- `can_create` – Can create new book instances.
- `can_edit` – Can edit existing book instances.
- `can_delete` – Can delete book instances.

These permissions are created via the `Meta.permissions` list in the `Book` model.

User roles are implemented using **groups** in the Django admin:

- **Viewers**
  - Permissions: `bookshelf.can_view`
- **Editors**
  - Permissions: `bookshelf.can_view`, `bookshelf.can_create`, `bookshelf.can_edit`
- **Admins**
  - Permissions: `bookshelf.can_view`, `bookshelf.can_create`, `bookshelf.can_edit`, `bookshelf.can_delete`
  - Typically also have `is_staff=True`.

The permissions are enforced in `bookshelf/views.py` using the `@permission_required` decorator:

- `book_list` → requires `bookshelf.can_view`
- `book_create` → requires `bookshelf.can_create`
- `book_edit` → requires `bookshelf.can_edit`
- `book_delete` → requires `bookshelf.can_delete`

To test:
1. Create users in the admin.
2. Assign them to the `Viewers`, `Editors`, or `Admins` groups.
3. Log in as each user and try to access the book views.



## Security Measures Implemented

This project follows several Django security best practices:

1. **Secure settings** (`LibraryProject/settings.py`)
   - `DEBUG = False` in production to avoid leaking sensitive information.
   - `SECURE_BROWSER_XSS_FILTER = True` and `SECURE_CONTENT_TYPE_NOSNIFF = True`
     to reduce XSS and content sniffing risks.
   - `X_FRAME_OPTIONS = "DENY"` to prevent clickjacking.
   - `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True` so cookies
     are only sent over HTTPS in production.

2. **Content Security Policy (CSP)**
   - Custom middleware (`LibraryProject/middleware.py`) adds a
     `Content-Security-Policy` header limiting resources to this origin:
     `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;`

3. **CSRF protection**
   - `CsrfViewMiddleware` is enabled in `MIDDLEWARE`.
   - All POST forms include `{% csrf_token %}` (e.g. `form_example.html`).
   - Views handling POST requests are decorated with `@csrf_protect`.

4. **SQL injection prevention and safe input handling**
   - All database access uses Django ORM, e.g.:
     `Book.objects.filter(...)` instead of raw SQL.
   - User input (e.g. search queries, form data) is handled via Django forms:
     `BookForm` and `BookSearchForm` in `bookshelf/forms.py`, with validation
     and cleaned data before use in queries.
