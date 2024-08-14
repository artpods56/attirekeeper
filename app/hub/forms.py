from django import forms
from .models import Template, Listing, Measurement, Photo, Brand, Purchase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, HTML, Button
from crispy_forms.bootstrap import InlineRadios, Tab, TabHolder, Field, Div
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.urls import reverse
from .widgets import CustomSelectWidget

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            "name",
            "description",
        )

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {
                "class": "name-input",
            }
        )
        self.fields["description"].widget.attrs.update({"class": "description-input"})
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset('Template Details',
                    Field('name'),
                    Field('description'),
                ),
            )

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "size",
            "flaws",
            "brand",
            "price",
            "condition",
            "category",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["size"].widget = CustomSelectWidget(
            choices_map=Listing.size_choices_map, choices=Listing.size_choices
        )

        self.fields["size"].widget.attrs["disabled"] = True

        self.helper = FormHelper()
        self.helper.form_id = "id-listing-form"
        self.helper.form_method = "post"
        self.helper.form_class = "form-floating"


        self.helper.layout = Layout(
            Fieldset(
                "Details",
                Row(
                    Column(
                        FloatingField("title"),
                        FloatingField(
                            "description", css_class="custom-textarea", rows=8
                        ),
                        FloatingField("flaws"),
                    ),
                    Column(
                        TabHolder(
                            Tab(
                                "General Information",
                                Row(
                                    Column(
                                        FloatingField("brand", template='bootstrap5/custom_crispy_group_field.html'),
                                        FloatingField("condition"),
                                        FloatingField("price"),
                                    ),
                                    css_class="mt-4",
                                ),
                            ),
                            Tab(
                                "Measurements",
                                Row(
                                    Column(
                                        FloatingField(
                                            "category", css_class="form-select"
                                        ),
                                    ),
                                    Column(FloatingField("size")),
                                ),
                                HTML(
                                    "{% include 'hub/components/measurements_form.html' %}"
                                ),
                                css_class="mt-4",
                            ),
                        ),
                    ),
                ),
            ),
            Fieldset(
                "Photos",
                HTML("{% include 'hub/components/images_form.html' %}"),
                Div(
                    HTML(" {% if task == 'create' %} <button type='submit' onclick='setFormAction(`{% url 'items_router' task='create' %}`)' class='btn btn-primary'>Create</button> {% else %} <button type='submit' onclick='setFormAction(`{% url 'items_router' task='update' id=id %}`)' class='btn btn-primary'>Update</button> {% endif %}"), 
                    css_class="mt-4"
                ),
            ),
        )


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
        fields = ["image"]
        file_field = MultiplePhotosField(required=False)
        labels = {"image": "Listing Images"}

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update(
            {"class": "photo-input", "multiple": True, "accept": "image/*"}
        )


class MeasurementsForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            "width",
            "length",
            "shoulder_width",
            "sleeve_length",
            "waist",
            "hip",
            "inseam",
        ]

    def __init__(self, *args, **kwargs):
        super(MeasurementsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"placeholder": "cm"})

        self.helper = FormHelper()
        self.helper.form_id = "id-measurements-form"
        self.helper.form_method = "post"
        self.helper.form_class = "form-floating"


class PurchaseForm(forms.ModelForm):
    
    title = forms.CharField()
    
    bought_at = forms.DateField(
        widget = forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'}),
        required=False
    )
    
    sold_at = forms.DateField(
        widget = forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'}),
        required=False
    )
    class Meta:
        model = Purchase
        fields = ['bought_for', 'bought_at', 'sold_at', 'sold_for', 'sold']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('''
            <table>    
            <tr>
                <td class="bs-checkbox">
                    <input type="checkbox" name="btSelectItem" disabled/>
                </td>
                <td>
                    <span class="text">new record</span>
                </td>
            '''),
            HTML('<td>'),
            Field('title', wrapper_class='test-class', template = 'bootstrap5/custom_crispy_field.html'),
            HTML('</td><td>'),
            Field('bought_for', wrapper_class='mb-0', template = 'bootstrap5/custom_crispy_field.html'),
            HTML('</td><td>'),
            Field('bought_at', wrapper_class='mb-0', template = 'bootstrap5/custom_crispy_field.html'),
            HTML('</td><td>'),
            Field('sold_at', wrapper_class='mb-0', template = 'bootstrap5/custom_crispy_field.html'),
            HTML('</td><td>'),
            Field('sold_for', wrapper_class='mb-0', template = 'bootstrap5/custom_crispy_field.html'),
            HTML('</td><td>'),
            Field('sold', wrapper_class='mb-0', template = 'bootstrap5/custom_crispy_checkbox.html'),
            HTML('</td></tr></table>')
        )
        for field in self.fields.values():
            field.label = False
        
    def save(self, commit=True):
        purchase = super().save(commit=False)
        listing = Listing(title=self.cleaned_data['title'])
        if commit:
            listing.save()
            purchase.listing_id = listing
            purchase.save()
        return purchase, listing