[![Build Status](https://travis-ci.org/ambitioninc/django-user-guide.png)](https://travis-ci.org/ambitioninc/django-user-guide)
##Django User Guide


Django User Guide is a `django>=1.6` app that shows configurable, single-pane HTML guides to users. Showing a guide to all of your users is as easy as
creating a `Guide` object and linking them to your users. Use the convenient `{% user_guide %}` template tag where you want guides to appear and Django User Guide does the rest. When a user visits a page containing the template tag, they are greeted with relevant guides. Django User Guide decides what guide(s) a user needs to see and displays them in modal window with controls for cycling through those guides. Django User Guide tracks plenty of meta-data: creation times, guide importance, if the guide has been finished by specific users, finished times, etc.

## Guide

First you will need to create a `Guide` object. A `Guide` object consists of:

#### guide_name (required, max_length=64, unique)

This is a semantic, unique identifier for a guide. Allows for easy identification and targeted filtering.

#### html

The markup for the guide. Use this field to communicate with your users in a meaningful way.
Note that the data in this field is marked as safe before output, so it would be a bad idea to put untrusted data into it.

#### guide_tag (default='all')

A custom tag for grouping several guides together. Specifically designed to be used for filtering. If you had `my_guide_tag_list = ['welcome', 'onboard']` in your context, you would use `{% user_guide guide_tags=my_guide_tag_list %}` to show users all guides with tags 'welcome' and 'onboard' specifically.

### guide_importance (default=0)

A number representing the importance of the guide. Guides with a higher `guide_importance` are shown first. Guides are always sorted by `guide_importance`, then `creation_time`.

### guide_type (default='Window')

The rendering type for the guide. Only a modal window is currently supported. Future support for positioned coach-marks and other elements is planned.

### creation_time (auto_now_add=True)

Stores the current datetime when a `Guide` is created.

```python
from user_guide.models import Guide

Guide.objects.create(html='<div>Hello Guide!</div>', guide_name='First Guide', guide_importance=5)
```

## GuideInfo

The next step is creating `GuideInfo` objects. These are used to connect a `Guide` to a ``User`. A `GuideInfo` object consists of:

### user (required)

The `User` that should see a `Guide`. Any number of `User`s can be pointed to a `Guide`.

### guide (required)

The `Guide` to show a `User`. Any number of `Guide`s can be tied to a `User`.

### is_finished (default=False)

Marked true when the `User` has completed some [finishing criteria](#finishing-criteria). Also by default, users are only shown `Guide`s with `is_finished=False`.

### finished_time

When the finishing criteria is met, the value of `datetime.utcnow()` is stored.




