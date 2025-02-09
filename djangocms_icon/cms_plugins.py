# -*- coding: utf-8 -*-
import re

from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import IconForm
from .models import Icon


class IconPlugin(CMSPluginBase):
    model = Icon
    form = IconForm
    name = _('Icon')
    allow_children = True
    text_enabled = True

    fieldsets = [
        (None, {
            'fields': (
                'icon', 'label',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'template',
                'attributes',
            )
        }),
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_icon/{}/icon.html'.format(instance.template)

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(IconPlugin)
