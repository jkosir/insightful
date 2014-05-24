import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Avg
from django.http import HttpResponse
from django.utils.datastructures import SortedDict
from django.views.generic import View

from djangular.views.mixins import JSONResponseMixin
from core.mixins import ChartsUtilityMixin, AngularAppMixin
from core.helpers import cache_until_midnight


class MonthlyChartView(AngularAppMixin, JSONResponseMixin, ChartsUtilityMixin, View):
    num_days = 30
    SERIES = (
        ('page_views', 'Page views'),
        ('visits', 'Visitors'),
        ('unique_visitors', 'Unique visitors'),
        ('avg_duration', 'Average view duration'),
        ('avg_active_duration', 'Average engagement time'),
        ('actions_per_visit', 'Actions per visit')
    )
    SERIES_DICT = dict(SERIES)

    def dispatch(self, *args, **kwargs):
        datasets = json.loads(self.request.body).get('datasets')

        for dataset in datasets:
            if dataset not in self.SERIES_DICT.keys():
                return HttpResponse(status=400)  # Bad request

        out_data = {}
        for dataset in datasets:
            serie = getattr(self, dataset)()
            out_data[dataset] = serie.values()
            out_data['start_date'] = serie.keys()[0]

        response = HttpResponse(json.dumps(out_data, cls=DjangoJSONEncoder))
        response['Content-Type'] = 'application/json;charset=UTF-8'
        response['Cache-Control'] = 'no-cache'
        return response

    @cache_until_midnight
    def page_views(self):
        return self.group_by_date(self.pageviews, 'view_timestamp', Count('pk'))

    @cache_until_midnight
    def visits(self):
        return self.group_by_date(self.sessions, 'timestamp', Count('pk'))

    @cache_until_midnight
    def unique_visitors(self):
        return self.group_by_date(self.sessions, 'timestamp', Count('user__pk', distinct=True))

    @cache_until_midnight
    def avg_duration(self):
        return self.group_by_date(self.pageviews, 'view_timestamp', Avg('duration'))

    @cache_until_midnight
    def avg_active_duration(self):
        return self.group_by_date(self.pageviews, 'view_timestamp', Avg('active_duration'))

    @cache_until_midnight
    def actions_per_visit(self):
        actions = SortedDict()
        views = self.page_views()
        visits = self.visits()
        for key in views:
            if visits[key] != 0:
                actions[key] = views[key] / visits[key]
            else:
                actions[key] = 0
        return actions
