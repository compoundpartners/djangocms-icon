# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    show_pro_icons = forms.CheckboxField(
        'Show Pro Icons', required=False, initial=False
    )
    show_duotone_icons = forms.CheckboxField(
        'Show Duotone icons', required=False, initial=False
    )
    enable_color = forms.CheckboxField(
        'Enable color input', required=False, initial=False
    )
    enable_size = forms.CheckboxField(
        'Enable size input', required=False, initial=False
    )

    def to_settings(self, data, settings):
        settings['DJANGOCMS_ICON_SHOW_PRO_ICONS'] = int(data['show_pro_icons'])
        settings['DJANGOCMS_ICON_SHOW_DUOTONE_ICONS'] = int(data['show_duotone_icons'])
        settings['DJANGOCMS_ICON_ENABLE_COLOR'] = int(data['enable_color'])
        settings['DJANGOCMS_ICON_ENABLE_SIZE'] = int(data['enable_size'])
        return settings
