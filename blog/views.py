from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.all()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1  # Увеличиваем счетчик
        obj.save(update_fields=["views_count"])
        return obj


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")


def unpublish_product():
    return None


def products_by_category_view():
    return None