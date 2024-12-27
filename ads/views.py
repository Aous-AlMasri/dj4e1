from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from .models import Ad, Comment
from django.urls import reverse_lazy, reverse
from .forms import CreateForm, CommentForm

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class AdListView(OwnerListView):
    model = Ad

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get(self, request,  pk):
        ad = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=ad).order_by("-updated_at")
        comment_form = CommentForm()
        ctx = {"ad" : ad, "comments" : comments, "comment_form" : comment_form}
        return render(request, self.template_name, ctx)

class AdCreateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:all")

    def get(self, request):
        form = CreateForm()
        ctx = {"form" : form}
        return render(request, self.template_name, ctx)
    
    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {"form" : form}
            return render(request, self.template_name, ctx)
        
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()

        return redirect(self.success_url)
    
class AdUpdateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:all")

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {"form" : form}
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {"form" : form}
            return render(request, self.template_name, ctx)
        
        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    success_url = reverse_lazy("ads:all")

class AdCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST["comment"], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse("ads:ad_detail", args=[pk]))

class AdCommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"
    def get_success_url(self):
        ad = self.object.ad
        return reverse("ads:ad_detail", args=[ad.id])


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response["content-type"] = ad.content_type
    response["content-length"] = len(ad.picture)
    response.write(ad.picture)
    return response
