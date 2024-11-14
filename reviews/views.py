from django.views import generic
from django.urls import reverse_lazy
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


class BookListView(generic.ListView):
    model = Book
    template_name = "reviews/books.html"
    context_object_name = "books"

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre_choices'] = Book.GENRE_CHOICES
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "reviews/detail.html"

    def get_queryset(self):
        return Book.objects.all()


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ['review_text', 'rating']
    template_name = "reviews/add_review.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['review_text', 'rating']
    template_name = "reviews/edit_review.html"

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})


# class ReviewDeleteView(generic.DeleteView):
#     model = Review

#     def get_success_url(self):
#         return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    book_id = review.book.id
    review.delete()
    return redirect('book_detail', pk=book_id)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration succesful.")
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'reviews/register.html', {'form': form})