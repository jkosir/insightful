import django_select2

from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.templatetags.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.views import AuthenticationForm, login
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.models import modelform_factory
from django.views.generic import FormView, ListView, RedirectView

from core.mixins import LoginRequiredMixin, AngularAppMixin
from core.models import Website
from accounts.forms import EmailUserCreationForm


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return reverse_lazy('accounts:website_list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def dispatch(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).dispatch(*args, **kwargs)


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = EmailUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registration successful, you can now sign in.')
        return super(RegisterView, self).form_valid(form)


class AccountSettingsView(FormView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:website_list')

    def get_form(self, form_class):
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Password successfully changed.')
        return super(AccountSettingsView, self).form_valid(form)


class WebsiteListView(LoginRequiredMixin, ListView):
    template_name = 'accounts/websites.html'
    context_object_name = 'websites'

    def get_queryset(self):
        return self.request.user.website_set.order_by('pk')


class AddWebsiteView(LoginRequiredMixin, FormView):
    template_name = 'accounts/add_website.html'
    form_class = modelform_factory(Website, exclude=('user', ), widgets={'timezone': django_select2.Select2Widget()})
    success_url = reverse_lazy('accounts:website_list')

    def redirect_to_website_created(self, pk):
        return HttpResponseRedirect(reverse_lazy('accounts:website_created') + '?id={}'.format(pk))

    def form_valid(self, form):
        website = form.save(commit=False)
        website.user = self.request.user
        website.save()
        return self.redirect_to_website_created(website.pk)


class EditWebsiteView(AngularAppMixin, FormView):
    template_name = 'accounts/edit_website.html'
    form_class = modelform_factory(Website, exclude=('user', ), widgets={'timezone': django_select2.Select2Widget()})
    success_url = reverse_lazy('accounts:website_list')

    def get_form_kwargs(self):
        kwargs = super(EditWebsiteView, self).get_form_kwargs()
        kwargs['instance'] = self.get_website()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Website successfully edited.')
        return super(EditWebsiteView, self).form_valid(form)


class WebsiteCreatedView(TemplateView):
    template_name = 'accounts/website_created.html'

    def get_context_data(self, **kwargs):
        context = super(WebsiteCreatedView, self).get_context_data(**kwargs)
        context['jspath'] = self.request.build_absolute_uri(static('js/insightful.min.js'))
        context['report'] = self.request.build_absolute_uri(reverse('report'))
        if 'id' in self.request.GET:
            context['id'] = self.request.GET['id']
        else:
            context['id'] = '"YOUR WEBSITE ID"'

        return context


