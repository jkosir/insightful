from django.db.models import Avg
from django.views.generic import View

from djangular.views.mixins import JSONResponseMixin, allowed_action
from core.mixins import AngularAppMixin, ChartsUtilityMixin
from core.helpers import cache_cbv_method_until_midnight
from core.models import ContentInteraction


class EngagementJSONView(AngularAppMixin, ChartsUtilityMixin, JSONResponseMixin, View):

    @allowed_action
    def get_data(self, in_data):
        return {'content': self.tracked_content_avg_duration()}

    @cache_cbv_method_until_midnight
    def tracked_content_avg_duration(self):
        interactions = ContentInteraction.objects.values_list('page_view__path', 'content__name')
        interactions = interactions.filter(page_view__view_timestamp__gte=self.past_timestamp(days=5))
        avg_duration_data = interactions.annotate(avg=Avg('duration'))

        pages = {}
        for values in avg_duration_data:
            if not values[0] in pages:
                pages[values[0]] = []
            pages[values[0]].append([values[1], values[2]])

        pageviews = self.pageviews.filter(view_timestamp__gte=self.past_timestamp(days=5))
        total_active_time = pageviews.values('path').annotate(avg=Avg('active_duration')).order_by()
        for values in total_active_time:
            if values['path'] in pages:
                # Other = Total active time minus sum of active time of every tracked content
                # Only include if other > 0, can be less than 0 from quick scrolling and short views
                avg_total = values['avg']
                sum_avg = sum(x[1] for x in pages[values['path']])
                other = avg_total - sum_avg
                if other > 0:
                    pages[values['path']].append([u'Other', other])

        data = {}  # Limit to 3 pages
        for key in pages.keys()[:3]:
            data[key] = pages[key]
        return data









