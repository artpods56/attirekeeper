from django import forms
from .models import Template, Listing, Measurements, Photo

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ('name', 'description',)
        
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'name-input'})
        self.fields['description'].widget.attrs.update({'class': 'description-input'})
        
        
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'size', 'flaws', 'brand', 'price', 'condition', 'category']


class MultiplePhotosInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiplePhotosField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiplePhotosInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        file_field = MultiplePhotosField(required=False)
        
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'photo-input',
                                                  'multiple': True,
                                                  'accept': 'image/*'})

class MeasurementsForm(forms.ModelForm):
    class Meta:
        model = Measurements
        fields = ['width', 'length', 'shoulder_width', 'sleeve_length', 'waist', 'hip', 'inseam']