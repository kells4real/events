from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
import io
from django.core.files.storage import default_storage as storage


def get_profile_filename(instance, filename):
    title = instance.user
    slug = slugify(title)
    return "profile_pics/{}/dukeweb_{}".format(slug, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=get_profile_filename)
    bio = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(unique=True)

    ABI = 'ABI'
    ADA = 'ADA'
    AKW = 'AKW'
    ANA = 'ANA'
    BAU = 'BAU'
    BAY = 'Bayelsa State'
    BEN = 'Benue State'
    BON = 'Borno State'
    CRR = 'Cross River State'
    DEL = 'Delta State'
    EBO = 'Ebonyi State'
    ENU = 'Enugu State'
    EDO = 'Edo State'
    ABJ = 'FCT - Abuja'
    GOM = 'Gombe State'
    IMO = 'Imo State'
    KAD = 'Kaduna State'
    KAN = 'Kano State'
    JIG = 'Jigawa'
    KAT = 'Katsina State'
    KEB = 'Kebbi State'
    KOG = 'Kogi State'
    KWA = 'Kwara State'
    LAG = 'Lagos State'
    NAS = 'Nasarawa State'
    NIG = 'Niger State'
    OGU = 'Ogun State'
    OND = 'Ondo State'
    OSU = 'Osun'
    OYO = 'Oyo State'
    PLA = 'Plateau State'
    RIV = 'Rivers State'
    SOK = 'Sokoto State'
    TAR = 'Taraba State'
    YOB = 'Yobe State'
    ZAM = 'Zamfara State'


    states = (
        (ABI,  'Abia'),
        (ADA, 'Adamawa'),
        (AKW, 'Akwa-Ibom'),
        (ANA, 'Anambra'),
        (BAU, 'Bauchi'),
        (BAY, 'Bayelsa'),
        (BEN, 'Benue'),
        (BON, 'Borno'),
        (CRR, 'Cross'),
        (DEL, 'Delta'),
        (EBO, 'Ebonyi'),
        (ENU, 'Enugu'),
        (EDO, 'Edo'),
        (ABJ, 'FCT - Abuja'),
        (GOM, 'Gombe'),
        (IMO, 'Imo'),
        (JIG, 'Jigawa'),
        (KAD, 'Kaduna'),
        (KAN, 'Kano'),
        (KAT, 'Katsina'),
        (KEB, 'Kebbi'),
        (KOG, 'Kogi'),
        (KWA, 'Kwara'),
        (LAG, 'Lagos'),
        (NAS, 'Nasarawa'),
        (NIG, 'Niger'),
        (OGU, 'Ogun'),
        (OND, 'Ondo'),
        (OSU, 'Osun'),
        (OYO, 'Oyo'),
        (PLA, 'Plateau'),
        (RIV, 'Rivers'),
        (SOK, 'Sokoto'),
        (TAR, 'Taraba'),
        (YOB, 'Yobe'),
        (ZAM, 'Zamfara')
    )

    state = models.CharField(
        max_length=100,
        choices=states,
        default=ABI,
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.slug)])
            
    def _get_unique_slug(self):
        slug = slugify(self.user)
        unique_slug = slug
        num = 1
        if Profile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
        #
        # img_read = storage.open(self.image.name, 'r')
        # img = Image.open(img_read)
        #
        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     in_mem_file = io.BytesIO()
        #     img.save(in_mem_file, format='JPEG')
        #     img_write = storage.open(self.image.name, 'w+')
        #     img_write.write(in_mem_file.getvalue())
        #     img_write.close()
        #
        # img_read.close()

