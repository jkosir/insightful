import datetime
import json

from core.helpers import get_date_truncate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import Http404
from django.utils import timezone
from django.utils.datastructures import SortedDict
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from core.models import Website, PageView, Session
from overview.helpers import daterange


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AngularAppMixin(LoginRequiredMixin):
    def get_website(self):
        try:
            website = Website.objects.get(pk=self.kwargs['website_id'])
        except Website.DoesNotExist:
            raise Http404('No such website.')
        if website.user != self.request.user:
            raise PermissionDenied('You don\'t have permission to view this website.')
        return website

    def website_to_json(self, website):
        return mark_safe(json.dumps(model_to_dict(website, exclude=('timezone', ))))


class ChartsUtilityMixin(object):
    num_days = None

    @property
    def pageviews(self):
        return PageView.objects.filter(session__website=self.kwargs['website_id'])

    @property
    def pageviews_today(self):
        return self.pageviews.filter(view_timestamp__gt=self.today_midnight())

    @property
    def pageviews_yesterday(self):
        return self.pageviews.filter(view_timestamp__lte=self.today_midnight(),
                                     view_timestamp__gte=self.today_midnight() - timezone.timedelta(days=1))

    @property
    def sessions(self):
        return Session.objects.filter(website=self.kwargs['website_id'])

    @property
    def sessions_today(self):
        return self.sessions.filter(timestamp__gt=self.today_midnight())

    @property
    def sessions_yesterday(self):
        return self.sessions.filter(timestamp__lt=self.today_midnight(),
                                    timestamp__gt=self.today_midnight() - timezone.timedelta(days=1))

    def past_timestamp(self, **kwargs):
        return timezone.now().astimezone(self.get_website().timezone) - timezone.timedelta(**kwargs)

    def today_midnight(self):
        """
        Returns datetime, today at 00:00 am
        One might use now.date(), but that removes timezone data
        """
        return timezone.now().astimezone(self.get_website().timezone).replace(hour=0, minute=0, second=0)

    def seconds_until_midnight(self):
        now = timezone.now().astimezone(self.get_website().timezone)
        midnight = now.replace(hour=23, minute=59, second=59)
        diff = (midnight-now).total_seconds()
        return int(diff) + 60

    def yesterday_midnight(self):
        return self.today_midnight() - timezone.timedelta(days=1)

    def group_by_date(self, queryset, timestamp_field, aggregation_function):
        """
        Take given queryset, filter by website_id, group by day on timestamp_field
        with aggregation_function for last num_days days
        """
        end_date = self.today_midnight()
        truncate_date = get_date_truncate('day', timestamp_field, self.get_website().timezone)

        queryset = queryset.extra({'date': truncate_date})
        queryset = queryset.filter(**{timestamp_field + '__lt': end_date,
                                      timestamp_field + '__gt': end_date - timezone.timedelta(days=self.num_days)})
        # Need something else than a queryset for serialising
        data = list(queryset.values('date').annotate(aggregated_data=aggregation_function).order_by('date'))
        return self.add_zeros(data, self.num_days)

    def add_zeros(self, in_data, num_days):
        """
        Add count=0 on dates that aren't present in in_data list from self.group_by_date()
        """
        data = SortedDict()
        end_date = self.today_midnight().date()
        for date in daterange(end_date - timezone.timedelta(days=num_days), end_date):
            for pair in in_data:

                # Dates stored as datetime when using postgresql
                if isinstance(pair['date'], datetime.datetime):
                    if pair['date'].date() == date:
                        data[str(pair['date'].date())] = pair['aggregated_data']
                        break
                # Dates stored as string when using sqlite
                elif isinstance(pair['date'], unicode) or isinstance(pair['date'], str):
                    if pair['date'] == str(date):
                        data[pair['date']] = pair['aggregated_data']
                        break
                else:
                    raise StandardError('Can\'t figure out the date format in database. '
                                        'Not unicode, str or datetime')
            else:
                data[str(date)] = 0
        return data