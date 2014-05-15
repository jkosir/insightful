from content.views import ContentJSONView
from django.conf.urls import patterns, url
from django.contrib import admin
from engagement.views import EngagementJSONView
from monthlychart.views import MonthlyChartView

from overview.views import OverviewJSONView
from visitors.views import VisitorsJSONView

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^(?P<website_id>\d)/monthlychart/', MonthlyChartView.as_view(), name='monthlychart'),
   url(r'^(?P<website_id>\d)/overview/', OverviewJSONView.as_view(), name='overview'),
   url(r'^(?P<website_id>\d)/engagement/', EngagementJSONView.as_view(), name='engagement'),
   url(r'^(?P<website_id>\d)/visitors/', VisitorsJSONView.as_view(), name='visitors'),
   url(r'^(?P<website_id>\d)/content/', ContentJSONView.as_view(), name='content'),
)
