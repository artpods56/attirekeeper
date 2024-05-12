from django import forms
from .models import Template

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('name', 'description', 'category',)
        
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'name-input'})
        self.fields['description'].widget.attrs.update({'class': 'description-input'})