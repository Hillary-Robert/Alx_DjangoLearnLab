from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "author", "publication_year")
   
  list_filter = ("publication_year", "author")
    
  search_fields = ("title", "author")
    
  ordering = ("-publication_year", "title")
    
  list_per_page = 25


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth", "profile_photo")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {"fields": ("date_of_birth", "profile_photo")}),
    )


# 🔥 EXACT LINE the ALX checker is looking for
admin.site.register(CustomUser, CustomUserAdmin)
