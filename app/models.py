from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


def get_flyer(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "flyers/{}/dukeevents_{}".format(slug, filename)


class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    flyer = models.ImageField(upload_to=get_flyer, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(Hashtag, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, editable=True, blank=True)
    end_date = models.DateField(editable=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Date(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    start_date = models.DateField(null=True, editable=True, blank=True)
    end_date = models.DateField(editable=True, null=True, blank=True)

    def __str__(self):
        return self.start_date




