[![Build Status](https://travis-ci.org/ambitioninc/django-user-guide.png)](https://travis-ci.org/ambitioninc/django-user-guide)
##Django User Guide


Django User Guide is a `django>=1.6` app that shows configurable, self-contained HTML guides to users. Showing a guide to all of your users is as easy as
creating a `Guide` object and linking them to your users. Use the convenient `{% user_guide %}` template tag where you want guides to appear and Django User Guide does the rest. When a user visits a page containing the template tag, they are greeted with relevant guides. Django User Guide decides what guide(s) a user needs to see and displays them in a modal window with controls for cycling through those guides. Django User Guide tracks plenty of meta-data: creation times, guide importance, if the guide has been finished by specific users, finished times, etc.

## Table of Contents
1. [Installation](#installation)
1. [Guide](#guide)
1. [GuideInfo](#guide-info)
1. [Settings](#settings)
1. [Finishing Criteria](#finishing-criteria)
1. [Putting It All Together](#putting-it-all-together)

## <a name="installation">Installation</a>
To install Django User Guide:

```shell
pip install git+https://github.com/ambitioninc/django-user-guide.git@0.1
```

Add Django User Guide to your `INSTALLED_APPS` to get started:

settings.py

```python

# Simply add 'user_guide' to your installed apps.
# Django User Guide relies on several basic django apps.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'user_guide',
)
```

Add Django User Guide's urls to your project:

urls.py

```python
from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    url(r'^user-guide/', include('user_guide.urls')),
)
```

## <a name="guide">Guide</a>

First you will need to create one or more `Guide` objects. A `Guide` object consists of:

#### guide_name (required, max_length=64, unique)

This is a semantic, unique identifier for a `Guide`. Allows for easy identification and targeted filtering.

#### html

The markup for the `Guide`. Use this field to communicate with your users in a meaningful way.
Note that the data in this field is output with `{% html|safe %}`, so it would be a bad idea to put untrusted data in it.

#### guide_tag (default='all')

A custom tag for grouping several guides together. Specifically designed to be used for filtering. If you had `my_guide_tag_list = ['welcome', 'onboarding']` in your context, you would use `{% user_guide guide_tags=my_guide_tag_list %}` to show users all guides with tags 'welcome' and 'onboard' specifically.

#### guide_importance (default=0)

A number representing the importance of the `Guide`. `Guide` objects with a higher `guide_importance` are shown first. `Guide` objects are always sorted by `guide_importance`, then `creation_time`.

#### guide_type (default='Window')

The rendering type for the `Guide`. Only a modal window is currently supported. Future support for positioned coach-marks and other elements is planned.

#### creation_time (auto_now_add=True)

Stores the current datetime when a `Guide` is created.


## Guide Usage

```python
from user_guide.models import Guide

Guide.objects.create(
    html='<div>Hello Guide!</div>',
    guide_name='First Guide',
    guide_tag='onboarding',
    guide_importance=5
)
```

## <a name="guide-info">GuideInfo</a>

The next step is creating `GuideInfo` objects. These are used to connect a `Guide` to a `User`. A `GuideInfo` object consists of:

#### user (required)

The `User` that should see a `Guide`. Any number of `User` objects can be pointed to a `Guide`.

#### guide (required)

The `Guide` to show a `User`. Any number of `Guide` objects can be tied to a `User`.

#### is_finished (default=False)

Marked true when the `User` has completed some [finishing criteria](#finishing-criteria). By default, users are only shown `Guide` objects with `is_finished=False`.

#### finished_time

When the [finishing criteria](#finishing-criteria) is met, the value of `datetime.utcnow()` is stored.

## GuideInfo Usage

```python
from django.contrib.auth.models import User

from user_guide.models import Guide, GuideInfo

# Show the guide with the name 'First Guide' to the given user
guide = Guide.objects.get(guide_name='First Guide')
user = User.objects.get(id=1)

GuideInfo.objects.create(guide=guide, user=user)
```

## <a name="settings">Settings</a>

Django User Guide has several configurations that can finely tune your user guide experience.

#### USER_GUIDE_SHOW_MAX (default=10)

The maximum number of guides to show for a single page load. If a user had 20 possible guides and `USER_GUIDE_SHOW_MAX` was set to 5, only the first 5 (based on `guide_importance` and `creation_time`) guides would be shown.

#### USER_GUIDE_CSS_URL (default=None)

The path to a custom style sheet for Django User Guides. Added as a `link` tag immediately after the [django-user-guide.css](user_guide/static/user_guide/build/django-user-guide.css) source. If omitted, no extra style sheets are included. See [django-user-guide.css](user_guide/static/user_guide/build/django-user-guide.css) for class names to override.

#### USER_GUIDE_JS_URL (default=None)

The path to a custom script for Django User Guides. Added as a `script` tag immediately after the [django-user-guide.js](user_guide/static/user_guide/build/django-user-guide.js) source. If omitted, no extra scripts are included. See [django-user-guide.js](user_guide/static/user_guide/build/django-user-guide.js) for methods to override.

## Settings Usage

settings.py

```python
# Django User Guide settings
USER_GUIDE_SHOW_MAX = 5
USER_GUIDE_CSS_URL = 'absolute/path/to/style.css'
USER_GUIDE_JS_URL = 'absolute/path/to/script.js'
```

## <a name='finishing-criteria'>Finishing criteria</a>

Finishing criteria are rules to marking a guide as finished. By default, they only need to press the 'next' or 'done' button on a guide. This behavior can be overridden by creating a custom script and adding it to the USER_GUIDE_JS_URL setting. The custom script only needs to override the `window.DjangoUserGuide.isFinished` method.

custom-script.js

```js
    /**
     * @override isFinished
     * Only allows guides to be marked finished on Mondays.
     * @param {HTMLDivElement} item - The item to check.
     * @returns {Boolean}
     */
    window.DjangoUserGuide.isFinished = function(item) {
        if ((new Date()).getDay() === 1) {
            return true;
        }
        return false;
    };
```

settings.py

```python
USER_GUIDE_JS_URL = 'path/to/custom-script.js'
```

## <a name="putting-it-all-together">Putting It All Together</a>

Assuming you have created some `Guide` and `GuideInfo` objects, this is how you would
show your users their relevant guides.

views.py

```python
from django.views.generic import TemplateView

class CoolView(TemplateView):
    template_name = 'cool_project/cool_template.html'

    def get_context_data(self, **kwargs):
        context = super(CoolView, self).get_context_data(**kwargs)
        context['cool_guide_tags'] = ['general', 'welcome', 'onboarding']
        return context
```

templates/cool_project/cool_template.html

```html
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Hello User Guides</title>
    </head>
    <body>
        {% load user_guide_tags %}
        {% user_guide guide_tags=cool_guide_tags %}
        <h1>Hello User Guides!</h1>
    </body>
</html>
```
