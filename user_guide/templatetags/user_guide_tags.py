"""
Template tag for displaying user guides.
"""
from django import template
from django.conf import settings
from django.template import loader

from user_guide.models import GuideInfo


register = template.Library()

# The maximum number of guides to show per page
USER_GUIDE_SHOW_MAX = getattr(settings, 'USER_GUIDE_SHOW_MAX', 10)

# The url to any custom CSS
USER_GUIDE_CSS_URL = getattr(
    settings,
    'USER_GUIDE_CSS_URL',
    None
)

# The url to any custom JS
USER_GUIDE_JS_URL = getattr(
    settings,
    'USER_GUIDE_JS_URL',
    None
)


@register.simple_tag(takes_context=True)
def user_guide(context, *args, **kwargs):
    """
    Creates html items for all appropriate user guides.

        Kwargs:
            guide_name: A string name of a specific guide.
            guide_tags: An array of string guide tags.
            limit: An integer maxmimum number of guides to show at a single time.

        Returns:
            An html string containing the user guide scaffolding and any guide html.
    """
    user = context['request'].user if 'request' in context and hasattr(context['request'], 'user') else None

    if user and user.is_authenticated():  # No one is logged in
        limit = kwargs.get('limit', USER_GUIDE_SHOW_MAX)
        filters = {
            'user': user,
            'is_finished': False
        }

        # Handle special filters
        if kwargs.get('guide_name'):
            filters['guide__guide_name'] = kwargs.get('guide_name')
        if kwargs.get('guide_tags'):
            filters['guide__guide_tag__in'] = kwargs.get('guide_tags')

        # Set the html
        html = ''.join((
            '<div data-guide="{0}" class="django-user-guide-item">{1}</div>'.format(
                guide_info.id,
                guide_info.guide.html
            ) for guide_info in GuideInfo.objects.select_related('guide').filter(**filters).only('guide')[:limit]
        ))

        # Return the rendered template with the guide html
        return loader.render_to_string('user_guide/window.html', {
            'html': html,
            'css_href': '{0}user_guide/build/django-user-guide.css'.format(settings.STATIC_URL),
            'js_src': '{0}user_guide/build/django-user-guide.js'.format(settings.STATIC_URL),
            'custom_css_href': USER_GUIDE_CSS_URL,
            'custom_js_src': USER_GUIDE_JS_URL
        })
    else:
        return ''
