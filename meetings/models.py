from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time
import json
import what3words
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.core import serializers


WHAT_THREE_WORDS_API_KEY = settings.WHAT_THREE_WORDS_API_KEY
# Create your models here.
class MeetingDay(models.Model):
    value = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.value


class MeetingIntergroup(models.Model):
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.value


class MeetingSubType(models.Model):
    code = models.CharField(max_length=5, null=False, blank=False)
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.value}"


def get_time_band(meeting_time):
    time_band = ""
    if meeting_time > time(0, 0) and meeting_time <= time(12, 0):
        time_band = "morning"
    elif meeting_time > time(12, 0) and meeting_time <= time(18, 0):
        time_band = "afternoon"
    else:
        time_band = "evening"
    return time_band


def get_longitude_latitude(what_three_words):
    lat, lng = None, None
    geocoder = what3words.Geocoder(WHAT_THREE_WORDS_API_KEY)
    res = geocoder.convert_to_coordinates(what_three_words)
    if "coordinates" in res:
        lat = res["coordinates"]["lat"]
        lng = res["coordinates"]["lng"]
    return lat, lng


class Meeting(models.Model):
    MEETING_TYPES = [
        ("F2F", "Face To Face"),
        ("ONL", "Online"),
        ("HYB", "Hybrid"),
    ]
    SUBMISSION_TYPES = [
        ("new", "new"),
        ("existing", "existing"),
    ]
    type = models.CharField(
        max_length=3, choices=MEETING_TYPES, null=False, blank=False, default="F2F"
    )
    submission = models.CharField(
        max_length=10,
        choices=SUBMISSION_TYPES,
        null=False,
        blank=False,
        default="existing",
    )
    address = models.TextField(blank=True, max_length=300)
    code = models.IntegerField(blank=True, null=True, default=-1)
    days = models.ManyToManyField(to=MeetingDay, related_name="meeting_days")
    intergroup = models.ForeignKey(
        to=MeetingIntergroup,
        related_name="meeting_intergroup",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    online_link = models.URLField(max_length=1000, null=True, blank=True)
    online_password = models.CharField(max_length=50, null=True, blank=True)
    payment_details = models.TextField(null=True, blank=True)
    what_three_words = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(
        null=False, blank=False, default="doesnotexist@aalondon.com"
    )
    hearing = models.BooleanField(null=True, default=False)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    postcode = models.TextField(max_length=10, null=True, blank=True)
    duration = models.TextField(blank=True, max_length=20)
    title = models.TextField()
    wheelchair = models.BooleanField(null=True, default=False)
    day_number = models.IntegerField(blank=True, null=True)
    slug = AutoSlugField(populate_from=["title", "postcode", "time"], max_length=100)
    day_rank = models.IntegerField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    intergroup = models.CharField(blank=True, max_length=100, null=True)
    intergroup_id = models.IntegerField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    time_band = models.CharField(blank=True, max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    conference_url = models.URLField(max_length=1000, blank=True, null=True)
    types = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    sub_types = models.ManyToManyField(
        to=MeetingSubType, blank=True, related_name="meeting_categories"
    )
    published = models.BooleanField(null=False, blank=False, default=False)
    gso_opt_in = models.BooleanField(null=False, blank=False, default=False)
    xmas_open = models.BooleanField(null=False, blank=False, default=False)
    xmas_closed = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):

        return self.title

    @property
    def meeting_days(self):
        return ", ".join([str(p) for p in self.days.all()])

    @property
    def meeting_categories(self):
        return ", ".join([str(p) for p in self.sub_types.all()])

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)

        # save original values, when model is loaded from database,
        # in a separate attribute on the model
        instance._loaded_values = dict(zip(field_names, values))

        return instance

    @property
    def call_what_three_words(self):
        """Works out whether we need to call what_three_words"""
        if not self._state.adding and self.published:
            if self.what_three_words:
                if (
                    self._loaded_values["what_three_words"] != self.what_three_words
                    or not self.lat
                ):
                    return True
        return False

    def send_mail_to_gso_contacts(self):
        gso_contacts = EmailContact.objects.filter(update_to_gso=True)

        message = get_template("meetings/gso_email.html").render({"meeting": self})

        if gso_contacts:
            to_emails = [obj.email for obj in gso_contacts]
            email_message = EmailMessage(
                subject="Meeting Added/Updated to aa-london.com",
                body=message,
                from_email="AA-LONDON<info@aa-london.com>",
                to=to_emails,
                reply_to=["info@aa-london.com"],
            )
            email_message.content_subtype = "html"
            email_message.send()

    def send_mail_to_user(self):

        message = get_template("meetings/user_submission_email.html").render(
            {"meeting": self}
        )
        email_message = EmailMessage(
            subject="Meeting Added/Updated to aa-london.com",
            body=message,
            from_email="AA-LONDON<info@aa-london.com>",
            to=[self.email],
            bcc=['info@aa-london.com'],
            reply_to=["info@aa-london.com"],
        )
        email_message.content_subtype = "html"
        email_message.send()

    def save(self, *args, **kwargs):

        self.slug = slugify(f"{self.title} {self.time} {self.type} {self.id}")
        self.time_band = get_time_band(self.time)
        if self.call_what_three_words:
            self.lat, self.lng = get_longitude_latitude(self.what_three_words)
        super(Meeting, self).save(*args, **kwargs)
        # send email to gso
        if self.published:
            if self.gso_opt_in:
                self.send_mail_to_gso_contacts()

            try:
                if self._loaded_values["published"] != self.published:
                    self.send_mail_to_user()
            except AttributeError:
                pass

    def get_absolute_url(self):

        return reverse("meeting-detail", kwargs={"pk": self.pk})


class EmailContact(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=100)
    last_name = models.CharField(null=False, blank=False, max_length=100)
    organisation = models.CharField(null=False, blank=False, max_length=200)
    email = models.EmailField(
        null=False, blank=False, default="doesnotexist@aalondon.com"
    )
    update_to_gso = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.organisation}"
