from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


# def home(request):
#     posts = Post.objects.all()
#     context = {
#         'posts':posts
#     }
#     return render(request,'blog/home.html',context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    # def get_queryset(self):
    #     user = get_object_or_404(User,username=self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by('-date_posted')

    

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    redirect_field_name = 'redirect_to'
    #login_url = '/login/'
    #success_url = '/'


    def get_success_url(self):
        return reverse('post_detail',kwargs={'pk':self.object.id})

    # def get_success_url(self):
    #     return reverse('post_detail', kwargs={'pk': self.object.id})

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def form_valid(self,form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    redirect_field_name = 'redirect_to'
    #login_url = '/login/'
    #success_url = '/'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False            


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    # def get_success_url(self):
    #     return reverse('post_detail', kwargs={'pk': self.object.id})

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False  


def about(request):
    return render(request,'blog/about.html',{'title':'About'})
