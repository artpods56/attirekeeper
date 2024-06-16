from django import forms
from .models import Template, Listing, Measurement, Photo, Brand
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
        self.helper.form_action = reverse("upload")

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
                                        FloatingField("brand"),
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
                    Submit("submit", "Submit", css_class="btn btn-primary"),
                    css_class="mt-4",
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
