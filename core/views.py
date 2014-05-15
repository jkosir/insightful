import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.views.generic.base import TemplateView

from core.mixins import AngularAppMixin
from core.models import TrackerUser, PageView, Website, TrackedContent, ContentInteraction
from monthlychart.views import MonthlyChartView


class ReportView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        website = get_object_or_404(Website, pk=request.POST['id'])
        post = request.POST.copy()

        user, created = TrackerUser.objects.get_or_create(uuid=post['uuid'])
        if created:
            user.http_agent = request.META['HTTP_USER_AGENT']
            user.remote_addr = request.META['REMOTE_ADDR']
            user.mobile = request.mobile
            user.save()

        session = user.get_session(website)
        last_view = session.pageview_set.last()
        if last_view:
            last_view.duration = int((timezone.now() - last_view.view_timestamp).total_seconds())
            if 'i_active_time' in post:
                last_view.active_duration = post.pop('i_active_time')[0]
            last_view.save()

            for key in filter(lambda x: x.startswith('i_'), post):
                content, created = TrackedContent.objects.get_or_create(website=website, name=key[2:])
                ContentInteraction(content=content,
                                   page_view=last_view,
                                   duration=request.POST[key][0]).save()  # remove v_ prefix

        PageView(session=session, path=post['path']).save()
        return HttpResponse(status=204)  # Http No content


class AngularView(AngularAppMixin, TemplateView):
    template_name = 'core/app.html'

    def get_context_data(self, **kwargs):
        context = super(AngularView, self).get_context_data(**kwargs)
        website = self.get_website()
        context.update(static_url=settings.STATIC_URL,
                       website=website,
                       website_json=self.website_to_json(website),
                       series=mark_safe(json.dumps(MonthlyChartView.SERIES)))
        return context
