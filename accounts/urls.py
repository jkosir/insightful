from django.conf.urls import patterns, url

from accounts.views import LoginView, RegisterView, WebsiteListView, LogoutView, AddWebsiteView, WebsiteCreatedView, \
    AccountSettingsView, EditWebsiteView

urlpatterns = patterns('',
   url(r'^login/$', LoginView.as_view(), name='login'),
   url(r'^logout/$', LogoutView.as_view(), name='logout'),
   url(r'^account/$', AccountSettingsView.as_view(), name='settings'),
   url(r'^created/$', WebsiteCreatedView.as_view(), name='website_created'),
   url(r'^register/$', RegisterView.as_view(), name='register'),
   url(r'^websites/$', WebsiteListView.as_view(), name='website_list'),
   url(r'^addwebsite/$', AddWebsiteView.as_view(), name='add_website'),
   url(r'^editwebsite/(?P<website_id>\d)/$', EditWebsiteView.as_view(), name='edit_website'),
   url(r'^signup/$', RegisterView.as_view(), name='signup'),

)
