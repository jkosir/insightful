import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from timezone_field.fields import TimeZoneField

from ua_parser import user_agent_parser
from geoip.mixins import GeoIpMixin


class Website(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    url = models.URLField()
    timezone = TimeZoneField()

    def __unicode__(self):
        return self.name

    def view_count_today(self):
        today_midnight = timezone.now().astimezone(self.timezone).replace(hour=0, minute=0, second=0)
        return len(PageView.objects.filter(session__website=self,
                                           view_timestamp__gt=today_midnight))


class TrackerUser(GeoIpMixin, models.Model):
    uuid = models.CharField(max_length=50)
    mobile = models.BooleanField(default=False)
    http_agent = models.TextField()
    remote_addr = models.IPAddressField(default="0.0.0.0")
    country_code = models.CharField(max_length=10)
    country_name = models.CharField(max_length=255)

    def get_session(self, website):
        """
        Get current session or create and return new session if previous expired
        """
        current = self.session_set.filter(website=website).last()  # Sessions must be sorted by timestamp
        if current:
            if timezone.now() - current.timestamp < datetime.timedelta(seconds=60 * settings.MAX_PAGE_VIEW_DURATION):
                return current
        new = Session(user=self, website=website)
        new.save()
        return new

    @property
    def parsed_user_agent(self):
        user_agent_data = user_agent_parser.Parse(self.http_agent)

        return {'os': user_agent_data['os']['family'],
                'browser': user_agent_data['user_agent']['family'],
                'country': [self.country_code, self.country_name]}

    def save(self, *args, **kwargs):
        country = self.ip_lookup(self.remote_addr)
        self.country_code = country[0]
        self.country_name = country[1]

        super(TrackerUser, self).save(*args, **kwargs)


class Session(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('TrackerUser')
    website = models.ForeignKey('Website')

    class Meta:
        ordering = ('timestamp', )


class PageView(models.Model):
    session = models.ForeignKey('Session')
    path = models.CharField(max_length=255)
    view_timestamp = models.DateTimeField(auto_now_add=True)
    # Duration in seconds
    duration = models.IntegerField(default=0)
    active_duration = models.IntegerField(default=0)

    class Meta:
        ordering = ('view_timestamp', )


class TrackedContent(models.Model):
    website = models.ForeignKey('Website')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ContentInteraction(models.Model):
    page_view = models.ForeignKey('PageView')
    content = models.ForeignKey('TrackedContent')
    duration = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content.name