from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/add_review/", views.ReviewCreateView.as_view(), name="add_review"),
    path("review/<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="edit_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("login/", auth_views.LoginView.as_view(template_name="reviews/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register, name="register"),
]