from django.contrib import admin

from .models import Book, Review


# class BookAdmin(admin.ModelAdmin):
#     fields = ["title", "author", "genre", "description", "pub_date"]

admin.site.register(Book)
admin.site.register(Review)