from django import forms
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CustomSelectWidget(forms.Select):
    def __init__(self, choices_map: dict, *args, **kwargs):
        self.choices_map = choices_map
        super().__init__(*args, **kwargs)
        
    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)
        for group in groups:
            option_value = group[1][0]['value']
            if option_value in self.choices_map.keys():
                group[1][0]['attrs']['class'] = self.choices_map[option_value]
        return groups