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



# HTTPS and Secure Deployment Configuration

This project is configured to enforce HTTPS at the Django level using the
following settings in `LibraryProject/settings.py`:

- `SECURE_SSL_REDIRECT = True`  
  Redirects all HTTP requests to HTTPS.

- `SECURE_HSTS_SECONDS = 31536000`  
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`  
- `SECURE_HSTS_PRELOAD = True`  
  Enable HTTP Strict Transport Security (HSTS) so that browsers remember to
  always use HTTPS for this domain.

- `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`  
  Ensure that session and CSRF cookies are only sent over HTTPS connections.

- `X_FRAME_OPTIONS = "DENY"`  
  Protects against clickjacking by blocking the site from being embedded
  in an iframe.

- `SECURE_CONTENT_TYPE_NOSNIFF = True`  
  Prevents browsers from MIME-sniffing content types.

- `SECURE_BROWSER_XSS_FILTER = True`  
  Asks the browser to enable its XSS filtering to help block basic XSS attacks.

## Example Nginx Configuration for HTTPS

Below is an example of how an Nginx config could be set up for this project
using a TLS certificate (for example from Let's Encrypt):

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect all HTTP traffic to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com www.example.com;

    # Paths to SSL certificate and key files
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Pass requests to the Django app (via gunicorn/uwsgi etc.)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Real-IP $remote_addr;
    }
}



This satisfies the “Deployment Configuration: instructions / scripts for HTTPS” requirement.

---

## 3️⃣ Security Review – Short Report Text

Add this to `README.md` or create `security_review.md` in the same folder:

```markdown
# Security Review – HTTPS and Secure Settings

This project has been configured to use HTTPS and to apply several security
best practices:

1. **HTTPS Enforcement**
   - `SECURE_SSL_REDIRECT = True` ensures all HTTP requests are redirected
     to HTTPS so that data in transit is encrypted.
   - HSTS (`SECURE_HSTS_SECONDS = 31536000`,
     `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`,
     `SECURE_HSTS_PRELOAD = True`) tells browsers to remember that this
     site must only be accessed over HTTPS, which helps prevent protocol
     downgrade attacks and cookie hijacking.

2. **Secure Cookies**
   - `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` prevent
     session and CSRF cookies from being transmitted over plain HTTP. This
     reduces the risk of attackers stealing cookies on an unencrypted network.

3. **Secure Headers**
   - `X_FRAME_OPTIONS = "DENY"` protects against clickjacking by blocking
     the site from being embedded in iframes.
   - `SECURE_CONTENT_TYPE_NOSNIFF = True` stops browsers from trying to guess
     (“sniff”) the content type of responses, which can prevent some XSS and
     drive-by-download attacks.
   - `SECURE_BROWSER_XSS_FILTER = True` asks modern browsers to enable their
     built-in XSS protection.

4. **Remaining Considerations / Improvements**
   - In production, TLS certificates must be correctly installed at the web
     server or reverse proxy level (for example with Nginx and Let's Encrypt).
   - Monitoring and logging should be configured so that failed logins and
     suspicious activity can be detected.
   - Regular security updates for Django, Python, and system packages are
     required to keep the environment patched.
   - DEBUG must always stay `False` in production to avoid leaking sensitive
     information in error pages.

Overall, these measures significantly improve the security posture of the
application by enforcing encrypted transport, hardening cookie handling,
and adding defensive security headers.

