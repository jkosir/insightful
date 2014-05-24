from django.db.models import Count
from django.views.generic import View
from djangular.views.mixins import allowed_action, JSONResponseMixin

from core.mixins import AngularAppMixin, ChartsUtilityMixin
from core.helpers import cache_until_midnight


class OverviewJSONView(AngularAppMixin, ChartsUtilityMixin, JSONResponseMixin, View):

    @allowed_action
    def get_data(self, in_data):
        return {'views': self.view_count_today(),
                'visitors': self.visitor_count_today(),
                'unique_visitors': self.unique_visitor_count_today(),
                'mobile': self.mobile_percent(),
                'top_pages': self.top_pages()}

    def view_count_today(self):
        return len(self.pageviews_today.all())

    def visitor_count_today(self):
        return len(self.sessions_today.all())

    def unique_visitor_count_today(self):
        return len(set(self.sessions_today.values_list('user_id')))  # Turn list into a set to remove duplicates

    @cache_until_midnight
    def mobile_percent(self):
        pageviews = self.pageviews.filter(view_timestamp__gt=self.past_timestamp(days=5))
        if len(pageviews) == 0:
            return 0
        return int(100*len(self.pageviews.filter(session__user__mobile=True))/float(len(self.pageviews)))

    def top_pages(self):
        query = self.pageviews_today.values('path').annotate(count=Count('path')).order_by('-count')
        return list(query[:4])


