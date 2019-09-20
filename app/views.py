from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q

# Create your views here.


class EventDetailView(DetailView):

    model = Event
    template_name = 'app/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        return context


class Home(ListView):
    model = Event
    template_name = 'app/index.html'


class SearchResultsView(ListView):
    model = Event
    template_name = 'app/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        )
        return object_list


class EventCreate(CreateView):
    model = Event
    template_name = 'app/event_create.html'
    form_class = EventForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(EventCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = TicketTypeFormSet(self.request.POST)
        else:
            data['titles'] = TicketTypeFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(EventCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:event_detail', kwargs={'slug': self.object.slug})


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'app/event_create.html'

    def get_context_data(self, **kwargs):
        data = super(EventUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = TicketTypeFormSet(self.request.POST, instance=self.object)
        else:
            data['titles'] = TicketTypeFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(EventUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:event_detail', kwargs={'slug': self.object.slug})

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CollectionUpdate, self).dispatch(*args, **kwargs)


class EventDelete(DeleteView):
    model = Event
    template_name = 'app/confirm_delete.html'
    success_url = reverse_lazy('app:home')
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

