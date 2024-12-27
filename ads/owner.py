from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerListView(ListView):
 """ a """

class OwnerDetailView(DetailView):
 """ b """

class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        print("form_valid is called")

        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        print("update get_queryset is called")

        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        print("update get_queryset is called")

        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
