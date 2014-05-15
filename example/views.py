from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'example/index.html'


class TestView2(TemplateView):
    template_name = 'example/index2.html'



