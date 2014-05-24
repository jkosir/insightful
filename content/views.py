from django.db.models import Avg
from django.views.generic import View

from djangular.views.mixins import JSONResponseMixin, allowed_action
from core.mixins import AngularAppMixin, ChartsUtilityMixin
from core.helpers import cache_until_midnight
from core.models import ContentInteraction


class ContentJSONView(AngularAppMixin, ChartsUtilityMixin, JSONResponseMixin, View):
    num_days = 5
    start_date = None

    @allowed_action
    def get_data(self, in_data):
        interactions, start_date = self.interaction_history()
        return {'start_date': start_date,
                'interactions': interactions}

    @property
    def interactions(self):
        return ContentInteraction.objects.filter(content__website=self.get_website())

    def pages_with_tracked_content(self):
        path_pairs = self.interactions.values('page_view__path').annotate()
        return [x['page_view__path'] for x in path_pairs]

    def content_on_page(self, path):
        content_names = []
        query = self.interactions.filter(page_view__path=path).values('content__name').annotate()
        for pair in query:
            content_names.append(pair['content__name'])
        return content_names

    def group_interaction(self, path, name):
        return self.group_by_date(self.interactions.filter(page_view__path=path, content__name=name),
                                  'timestamp',
                                  Avg('duration'))

    @cache_until_midnight
    def interaction_history(self):
        start_date = None
        data = {}
        paths = self.pages_with_tracked_content()
        for path in paths:
            data[path] = {}
            for name in self.content_on_page(path):
                annotated_data = self.group_interaction(path, name)
                data[path][name] = annotated_data.values()
                start_date = annotated_data.keys()[0]
        return data, start_date