from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from datetime import time
import json
import base64
import what3words
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from django.core import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

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


def confirmation_link(pk, title, request):
    """
        NOTE: generate confirmation link containing meeting data. 

        @params
            pk - Meeting primary key.
            title - Meeting title.  
            request - HttpRequest

        @returns
            str - confirmation link. 
    """
    domain = request.build_absolute_uri('/')[:-1]
    token = base64.urlsafe_b64encode(json.dumps({"pk": pk, "title": title}).encode()).decode().rstrip("=")

    link = reverse("email-confirmation", kwargs={
        "token": token
    })

    return domain + f"{link}"


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
    EMAIL_CONFIRMED_TYPES = [
        ("CONFIRMED", "confirmed"),
        ("UNCONFIRMED", "unconfirmed"),
        ("PRE", "pre")
    ]
    type = models.CharField(
        max_length=3, choices=MEETING_TYPES, null=False, blank=False, default="F2F"
    )
    notes = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    submission = models.CharField(
        max_length=10,
        choices=SUBMISSION_TYPES,
        null=False,
        blank=False,
        default="existing",
    )
    title = models.TextField()
    location = models.TextField(blank=True, max_length=300)
    address = models.TextField(blank=True, max_length=300)
    postcode = models.TextField(max_length=10, null=True, blank=True)
    postcode_prefix = models.TextField(max_length=10, null=True, blank=True)
    intergroup = models.CharField(blank=True, max_length=100, null=True)
    what_three_words = models.CharField(max_length=100, null=True, blank=True)
    days = models.ManyToManyField(to=MeetingDay, related_name="meeting_days")
    code = models.IntegerField(blank=True, null=True, default=-1)
    time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    email = models.EmailField(
        null=False, blank=False, default="doesnotexist@aalondon.com"
    )
    email_confirmed = models.CharField(
        max_length=50, choices=EMAIL_CONFIRMED_TYPES, default="PRE")
    temporary_changes = models.TextField(max_length=1000, help_text="e.g. Please note that this meeting is closed on this day.", default="", blank=True)
    note_expiry_date = models.DateField(null=True, blank=True)
    tradition_7_details = models.TextField(null=True, blank=True)
    online_link = models.URLField(max_length=1000, null=True, blank=True)
    online_password = models.CharField(max_length=50, null=True, blank=True)
    sub_types = models.ManyToManyField(
        to=MeetingSubType, blank=True, related_name="meeting_categories"
    )
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    duration = models.TextField(blank=True, max_length=20)
    day_number = models.IntegerField(blank=True, null=True)
    slug = AutoSlugField(populate_from=["title", "postcode", "time"], max_length=100)
    day_rank = models.IntegerField(blank=True, null=True)
    group = models.TextField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    time_band = models.CharField(blank=True, max_length=10, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(null=False, blank=False, default=False)
    gso_opt_out = models.BooleanField(null=False, blank=False, default=False)
    updated_by = models.ForeignKey(to=User,null=True,on_delete=models.SET_NULL)

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
        if self.postcode:
            self.postcode_prefix = self.postcode[:-3].strip()
        super(Meeting, self).save(*args, **kwargs)
        # send email to gso
        if self.published:
            if not self.gso_opt_out:
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
