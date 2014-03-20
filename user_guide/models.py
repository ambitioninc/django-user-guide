from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


USER_GUIDE_HTML_MAX = getattr(settings, 'USER_GUIDE_HTML_MAX', 512)
USER_GUIDE_TAG_MAX = getattr(settings, 'USER_GUIDE_TAG_MAX', 64)


class Guide(models.Model):
    """
    Describes a guide to be tied to any number of users.
    """
    # The html that should be rendered in a guide.
    html = models.TextField(max_length=USER_GUIDE_HTML_MAX)
    # The type of guide to render. The only guide type currently supported is 'Window.'
    guide_type = models.CharField(max_length=16, choices=(('WINDOW', 'Window'),), default='WINDOW')
    # The name of the guide. Mainly for display purposes.
    guide_name = models.CharField(max_length=64, unique=True)
    # A tag for the given guide. For filtering purposes.
    guide_tag = models.CharField(max_length=USER_GUIDE_TAG_MAX, default='all')
    # An ordering parameter for the guide. To show a guide first, give it a larger guide_order.
    guide_order = models.IntegerField(default=0)
    # The creation time of the guide.
    creation_time = models.DateTimeField(auto_now_add=True)


class GuideInfo(models.Model):
    """
    Ties a guide to a user.
    """
    # The user that should see this guide.
    user = models.ForeignKey(User)
    # The guide that should be shown to the user.
    guide = models.ForeignKey(Guide)
    # Show the user the guide until it has been marked finished
    finished = models.BooleanField(default=False)
    # Save the finished time for convenience
    finished_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'guide')
