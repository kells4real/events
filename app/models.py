from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


def get_flyer(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "flyers/{}/dukeevents_{}".format(slug, filename)


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FeaturedEvent(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Featured Event"
        verbose_name_plural = "Featured Events"

    def _get_unique_slug(self):
        slug = slugify(self.name)
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


class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    flyer = models.ImageField(upload_to=get_flyer, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(Hashtag, on_delete=models.CASCADE, null=True, blank=True)
    venue = models.CharField(max_length=200, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    feat = models.ForeignKey(FeaturedEvent, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField(null=True, editable=True, blank=True)
    end_date = models.DateField(editable=True, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
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

        img = Image.open(self.flyer.path)

        if img.height > 896 or img.width > 640:
            output_size = (640, 896)
            img.thumbnail(output_size)
            img.save(self.flyer.path)

    class Meta:
        verbose_name_plural = "Events"


class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"


class Emails(models.Model):
    email_add = models.EmailField(null=True)

    def __str__(self):
        return self.email_add


