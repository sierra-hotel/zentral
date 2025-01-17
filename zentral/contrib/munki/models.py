import enum
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F
from django.urls import reverse
from zentral.contrib.inventory.models import BaseEnrollment


# configuration


class PrincipalUserDetectionSource(enum.Enum):
    company_portal = "Company portal"
    google_chrome = "Google Chrome"
    logged_in_user = "Logged-in user"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def accepted_sources(cls):
        return set(i.name for i in cls)


class Configuration(models.Model):
    name = models.CharField(max_length=255, unique=True)
    inventory_apps_full_info_shard = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=100
    )
    principal_user_detection_sources = ArrayField(
        models.CharField(max_length=64, choices=PrincipalUserDetectionSource.choices()),
        blank=True,
        default=list,
    )
    principal_user_detection_domains = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list
    )

    version = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("munki:configuration", args=(self.pk,))

    def save(self, *args, **kwargs):
        if not self.id:
            self.version = 0
        else:
            self.version = F("version") + 1
        super().save(*args, **kwargs)


# enrollment


class Enrollment(BaseEnrollment):
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "{}#enrollment-{}".format(self.configuration.get_absolute_url(), self.pk)

    def get_description_for_distributor(self):
        return "Zentral pre/postflight"


class EnrolledMachine(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    serial_number = models.TextField(db_index=True)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


# munki state


class MunkiState(models.Model):
    machine_serial_number = models.CharField(max_length=64, unique=True)
    munki_version = models.CharField(max_length=32, blank=True, null=True)
    user_agent = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(blank=True, null=True)
    sha1sum = models.CharField(max_length=40, blank=True, null=True)
    run_type = models.CharField(max_length=64, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True)
