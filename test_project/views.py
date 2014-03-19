from django.views.generic import TemplateView


class TestProjectView(TemplateView):
    template_name = 'test_project/test_project.html'

    def get_context_data(self, **kwargs):
        """
        Set any special context here to pass to the user_guides template tag.
        """
        context = super(TestProjectView, self).get_context_data(**kwargs)
        context['guide_tags'] = ['all']
        return context
