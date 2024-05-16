from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps

def get_model_fields(request, model_name):
    # if not request.is_ajax():
    #     raise Http404

    excluded_types = ['AutoField', 'ForeignKey', 'OneToOneField', 'DateTimeField']

    # Get the model class based on the model_name variable
    model = apps.get_model('hub', model_name)

    model_fields = [field.name for field in model._meta.get_fields()
                    if field.get_internal_type() not in excluded_types]

    return JsonResponse(model_fields, safe=False)
