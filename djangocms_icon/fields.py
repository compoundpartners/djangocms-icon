# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import json

from django.conf import settings
from django.db import models
from django.forms import fields, widgets
from django.template.loader import render_to_string
from django.utils.translation import ugettext

SHOW_PRO_ICONS = getattr(settings, 'DJANGOCMS_ICON_SHOW_PRO_ICONS', False)
SHOW_DUOTONE_ICONS = getattr(settings, 'DJANGOCMS_ICON_SHOW_DUOTONE_ICONS', False)
ENABLE_COLOR = getattr(settings, 'DJANGOCMS_ICON_ENABLE_COLOR', False)
ENABLE_SIZE = getattr(settings, 'DJANGOCMS_ICON_ENABLE_SIZE', False)
COLORS = getattr(settings, 'DJANGOCMS_ICON_COLORS', getattr(settings, 'JS_COLOR_PICKET_COLORS', []))
COLOR_MODE = getattr(settings, 'DJANGOCMS_ICON_COLOR_PICKET_MODE', getattr(settings, 'JS_COLOR_PICKET_MODE', 'both'))
try:
    from js_color_picker import __version__
    THERE_IS_COLOR_PICKER = True
except:
    COLOR_MODE = 'input'
    THERE_IS_COLOR_PICKER = False

class IconDict():
    iconset = icon = color = size = ''

    def __init__(self, value=None):
        if value is None:
            value = ''
        if isinstance(value, dict):
            self.iconset = value.get('iconset', '')
            self.icon = value.get('icon', '')
            self.color = value.get('color', '')
            self.size = value.get('size', '')
        elif isinstance(value, str):
            value = value.split(None, 3)
        if isinstance(value, (list, tuple)):
            self.iconset = value[0] if len(value) else ''
            self.icon = value[1] if len(value) > 1 else ''
            if len(value) > 2:
                if re.match('^#?((?:[0-F]{3}){1,2})$', value[2], re.IGNORECASE):
                    self.color = value[2]
                    self.size = value[3]
                else:
                    self.size = ' '.join(value[2:])

    def __str__(self):
        return ' '.join([self.iconset, self.icon])

    def all(self):
        return ' '.join([self.iconset, self.icon, self.color, self.size])

    def __len__(self):
        if self.size:
            return 4
        elif self.color:
            return 3
        elif self.icon:
            return 2
        elif self.iconset:
            return 1
        return 0


def get_iconsets():
    if SHOW_PRO_ICONS:
        default = (
            ('fontawesome5regular', 'far', 'Font Awesome 5 Regular', '5.10.2_pro'),
            ('fontawesome5solid', 'fas', 'Font Awesome 5 Solid', '5.10.2_pro'),
            ('fontawesome5brands', 'fab', 'Font Awesome 5 Brands', '5.10.2_pro'),
            ('fontawesome5light', 'fal', 'Font Awesome 5 Light', '5.10.2_pro'),
        )
        if SHOW_DUOTONE_ICONS:
            default += (
                ('fontawesome5duotone', 'fad', 'Font Awesome 5 Duotone', '5.10.2_pro'),
            )
    else:
        default = (
            ('fontawesome5regular', 'far', 'Font Awesome 5 Regular', '5.10.2'),
            ('fontawesome5solid', 'fas', 'Font Awesome 5 Solid', '5.10.2'),
            ('fontawesome5brands', 'fab', 'Font Awesome 5 Brands', '5.10.2'),
        )
    iconsets = getattr(settings, 'DJANGOCMS_ICON_SETS', default)
    current_iconsets = []
    for iconset in iconsets:
        if len(iconset) == 3:
            iconset = iconset + ('lastest',)
        current_iconsets.append(iconset)

    return tuple(current_iconsets)


class IconFieldWidget(widgets.TextInput):
    class Media:
        css = {
            'all': [
                'djangocms_icon/css/djangocms-icon.css',
            ]
        }
        js = [
            'djangocms_icon/js/dist/bundle.icon.min.js',
        ]
        if ENABLE_COLOR or ENABLE_SIZE:
            js = [
                'djangocms_icon/js/dist/bundle.icon.new.min.js',
            ]
        if THERE_IS_COLOR_PICKER and COLOR_MODE != 'input':
            css['all'].append('color-picker/color-picker.css')
            js.append('color-picker/color-picker2.js')

    def render(self, name, value, attrs=None, **kwargs):
        if value is None or value == '':
            value = IconDict()
        if not isinstance(value, IconDict):
            value = IconDict(value)
        iconsets = get_iconsets()
        active_iconset = iconsets[0]
        size = ''
        color = ''

        if value:
            selected_iconset = None

            for iconset in iconsets:
                if iconset[1] == value.iconset:
                    selected_iconset = iconset
                    break

            active_iconset = active_iconset if selected_iconset is None else selected_iconset

        rendered = render_to_string(
            'admin/djangocms_icon/widgets/icon.html',
            {
                'value': value.icon,
                'name': name,
                'iconset': active_iconset[0],
                'version': active_iconset[3],
                'prefix': active_iconset[1],
                'is_required': self.is_required,
                'iconsets': iconsets,
                'size': value.size,
                'color': value.color,
                'colors': json.dumps(COLORS),
                'color_mode': COLOR_MODE,
                'enable_color': ENABLE_COLOR,
                'enable_size': ENABLE_SIZE,
            },
        )

        return rendered


class IconField(fields.CharField):
    widget = IconFieldWidget
    DEFAULT = ''

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = self.DEFAULT
        kwargs.pop('coerce', None)
        kwargs.pop('max_length', None)
        kwargs.pop('widget', None)
        kwargs['widget'] = self.widget
        super(IconField, self).__init__(*args, **kwargs)


class Icon(models.CharField):
    default_field_class = IconField
    south_field_class = 'models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = ugettext('Icon')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Icon, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Icon, self).formfield(**defaults)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return IconDict(value)

    def to_python(self, value):
        if isinstance(value, IconDict):
            return value

        if value is None:
            return value

        return IconDict(value)

    def get_prep_value(self, value):
        if isinstance(value, IconDict):
            return value.all()
        return value
