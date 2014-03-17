from django.views.generic import TemplateView


class TestProjectView(TemplateView):
    template = 'test_project/test_project.html'
