from django.db.models import Sum, Avg, Count
from django.views.generic import View

from djangular.views.mixins import allowed_action, JSONResponseMixin
from core.helpers import cache_cbv_method_until_midnight
from core.mixins import AngularAppMixin, ChartsUtilityMixin


class VisitorsJSONView(AngularAppMixin, ChartsUtilityMixin, JSONResponseMixin, View):
    num_days = 30

    @allowed_action
    def get_data(self, in_data):
        return {'visitors': self.latest_visitors(),
                'report': self.yesterday_report(),
                'countries': self.countries(),
                'inbound': self.inbound_outbound_links(),
                'outbound': self.inbound_outbound_links(inbound=False)}

    def latest_visitors(self):
        visitors = []
        new_sessions = self.sessions.order_by('-timestamp')[:4]
        new_sessions = new_sessions.select_related('user').prefetch_related('pageview_set')

        for session in new_sessions:
            session_data = {'pages': [],
                            'timestamp': session.timestamp}
            session_data.update(session.user.parsed_user_agent)
            session_data.update(self.total_and_active_time(session))

            # Add viewed pages
            for pageview in session.pageview_set.all():
                session_data['pages'].append(pageview.path)

            visitors.append(session_data)

        return visitors

    def total_and_active_time(self, session):
        data = {
            'total_time': session.pageview_set.aggregate(sum=Sum('duration'))['sum'],
            'active_time': session.pageview_set.aggregate(sum=Sum('active_duration'))['sum']
        }
        return data

    @cache_cbv_method_until_midnight
    def yesterday_report(self):
        return {'visitors': len(self.sessions_yesterday),
                'pageviews': len(self.pageviews_yesterday),
                'unique_visitors': len(set(self.sessions_yesterday.values_list('user_id'))),  # Set to remove duplicates
                'avg_time': self.sessions_yesterday.annotate(sum=Sum('pageview__duration')).aggregate(avg=Avg('sum'))['avg'],
                'avg_engagement': self.sessions_yesterday.annotate(sum=Sum('pageview__active_duration')).aggregate(avg=Avg('sum'))['avg'],
                'date': self.past_timestamp(days=1)}

    @cache_cbv_method_until_midnight
    def countries(self):
        sessions = self.sessions.filter(timestamp__gt=self.past_timestamp(days=5))
        values = sessions.values('user__country_code', 'user__country_name')
        data = values.annotate(count=Count('user__country_code')).order_by('count')

        # Rename dictionary keys
        for element in data:
            element['code'] = element.pop('user__country_code')
            element['country'] = element.pop('user__country_name')

        return list(data)

    @cache_cbv_method_until_midnight
    def inbound_outbound_links(self, inbound=True):
        paths = {}
        sessions = self.sessions.prefetch_related('pageview_set').filter(timestamp__gt=self.past_timestamp(days=5),
                                                                         timestamp__lt=self.today_midnight())
        for session in sessions:
            if inbound:
                view_path = session.pageview_set.all()[0].path
            else:  # Outbound:
                view_path = session.pageview_set.all().reverse()[0].path
            if view_path in paths:
                paths[view_path] += 1
            else:
                paths[view_path] = 1
        return paths.items()





