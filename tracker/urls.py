from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from core.views import ReportView, AngularView


urlpatterns = patterns('',
   url(r'^$', TemplateView.as_view(template_name='website/home.html'), name='home'),
   url(r'^learnmore$', TemplateView.as_view(template_name='website/learnmore.html'), name='learnmore'),
   url(r'^report/$', ReportView.as_view(), name='report'),
   url(r'^accounts/', include('accounts.urls', namespace='accounts')),
   url(r'^app/(?P<website_id>\d)/', AngularView.as_view(), name='app'),  # angular app

   url(r'api/', include('core.apiurls', namespace='api')),
)
