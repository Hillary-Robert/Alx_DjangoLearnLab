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
