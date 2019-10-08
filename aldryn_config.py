# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    show_pro_icons = forms.CheckboxField(
        'Show Pro Icons', required=False, initial=False
    )

    def to_settings(self, data, settings):
        settings['DJANGOCMS_ICON_SHOW_PRO_ICONS'] = int(data['show_pro_icons'])
        return settings
