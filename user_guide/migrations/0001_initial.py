# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('html', models.TextField()),
                ('guide_type', models.CharField(max_length=16, default='WINDOW', choices=[('WINDOW', 'Window')])),
                ('guide_name', models.CharField(unique=True, max_length=64)),
                ('guide_tag', models.TextField(default='all')),
                ('guide_importance', models.IntegerField(default=0)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GuideInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('finished_time', models.DateTimeField(null=True, blank=True)),
                ('guide', models.ForeignKey(to='user_guide.Guide')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-guide__guide_importance', 'guide__creation_time'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='guideinfo',
            unique_together=set([('user', 'guide')]),
        ),
    ]
