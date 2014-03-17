from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


USER_GUIDE_HTML_MAX = settings.USER_GUIDE_HTML_MAX if hasattr(
    settings, 'USER_GUIDE_HTML_MAX'
) else 512
USER_GUIDE_CLASS_NAME_MAX = settings.USER_GUIDE_CLASS_NAME_MAX if hasattr(
    settings, 'USER_GUIDE_CLASS_NAME_MAX'
) else 512


Guide(models.Model):
    """
    Describes a guide to be tied to any number of users.
    """
    # The html that should be rendered in a guide.
    html = models.TextField(max_length=settings.USER_GUIDE_HTML_MAX or 512)
    # The class name of the view that should render a guide.
    view_class_name = models.CharField(max_length=settings.USER_GUIDE_CLASS_NAME_MAX or 512)
    # The type of guide to render. The only guide type currently supported is 'Window.'
    guide_type = models.ChoiceField(max_length=16, choices=('WINDOW', 'Window'), default='WINDOW')
    # The creation time of the guide.
    creation_time = models.DateTimeField(auto_now_add=True)


GuideInfo(models.Model):
    """
    Ties a guide to a user.
    """
    # The user that should see this guide.
    user = models.ForeignKey(User)
    # The guide that should be shown to the user.
    guide = models.ForeignKey(GuideTemplate)
    # Show the user the guide until it has been marked finished
    finished = models.BooleanField(default=False)
    # Save the finished time for convenience
    finished_time = models.DateTimeField(null=True, blank=True)


