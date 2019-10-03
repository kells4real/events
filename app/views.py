from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Create your views here.
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api import EventSerializer, UsersSerializer, EventDetailSerializer


# Api Class To List All Events or Create One
class EventApiList(APIView):

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)

    def post(self):
        pass


class EventApiDetail(APIView):

    def get(self, request, slug):
        event = Event.objects.get(slug=slug)
        serializer = EventDetailSerializer(event)

        return Response(serializer.data)

    def post(self):
        pass


class UsersApiList(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data)

    def post(self):
        pass


class EventDetailView(DetailView):

    model = Event
    template_name = 'app/event_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(EventDetailView, self).get_context_data(**kwargs)
    #     context['owner'] = self.request.user
    #
    #     return context


class Home(ListView):
    model = Event
    template_name = 'app/index.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['today'] = date.today()
        popular = FeaturedEvent.objects.get(slug='popular').event_set.order_by('end_date')
        ads = FeaturedEvent.objects.get(slug='ads').event_set.order_by('end_date')
        context.update({
            'popular': popular,
            'ads': ads,
            'year': datetime.now().year
        })

        return context

    def get_queryset(self):
        return Event.objects.all().order_by('category')


# class Category(ListView):
#     model = Hashtag
#     template_name = 'app/base.html'


def category_details(request, slug):
    category = Hashtag.objects.get(slug=slug)
    event = category.event_set.all()

    context = {
        "today": date.today(),
        "event": event,
        "category": category
    }
    return render(request, "app/category_details.html", context)


class SearchResultsView(ListView):
    model = Event
    template_name = 'app/search.html'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query) |
            Q(state__name__icontains=query) | Q(state__name__icontains=query + "state")
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['ads'] = FeaturedEvent.objects.get(slug='ads').event_set.order_by('end_date')

        return context


class EventCreate(LoginRequiredMixin, CreateView):
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

        messages.success(self.request, f'Thank You For Creating an Event. '
                         f'Your Post will be reviewed and you will be able to see it soon upon approval..')
        return super(EventCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:event_detail', kwargs={'slug': self.object.slug})


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('app:event_detail', kwargs={'slug': self.object.slug})


class EventDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'app/confirm_delete.html'
    success_url = reverse_lazy('app:home')
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

