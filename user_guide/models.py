from django.contrib.auth.models import User
from django.db import models


class Guide(models.Model):
    """
    Describes a guide to be tied to any number of users.
    """
    # The html that should be rendered in a guide.
    html = models.TextField()
    # The type of guide to render. The only guide type currently supported is 'Window.'
    guide_type = models.CharField(max_length=16, choices=(('WINDOW', 'Window'),), default='WINDOW')
    # The name of the guide. Mainly for display purposes.
    guide_name = models.CharField(max_length=64, unique=True)
    # A tag for the given guide. For filtering purposes.
    guide_tag = models.TextField(default='all')
    # An ordering parameter for the guide. To show a guide first, give it a larger guide_importance.
    guide_importance = models.IntegerField(default=0)
    # The creation time of the guide.
    creation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.guide_name


class GuideInfo(models.Model):
    """
    Ties a guide to a user.
    """
    # The user that should see this guide.
    user = models.ForeignKey(User)
    # The guide that should be shown to the user.
    guide = models.ForeignKey(Guide)
    # Has the guide been seen by a user?
    is_finished = models.BooleanField(default=False)
    # Save the finished time for convenience
    finished_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'guide')
        ordering = ['-guide__guide_importance', 'guide__creation_time']
