from rest_framework import serializers, viewsets
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('title', 'description', 'flyer', 'state', 'category', 'venue',
                  'start_date', 'end_date', 'start_time', 'end_time')


class EventDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('title', 'description', 'flyer', 'state', 'category', 'venue',
                  'start_date', 'end_date', 'start_time', 'end_time')


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')


# class EventViewSet(viewsets.ModelViewSet):
#
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

