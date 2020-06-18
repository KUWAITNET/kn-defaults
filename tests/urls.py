from django.http import HttpResponse
from django.urls import path
from django.views.decorators.debug import sensitive_post_parameters


@sensitive_post_parameters('password')
def success_func_view(request):
    return HttpResponse(content='Ok')


def error_func_view(request):
    x = 5 / 0
    return HttpResponse(content='Not Ok')


urlpatterns = [
    path('success_func_view', success_func_view, name='success_func_view'),
    path('error_func_view', error_func_view, name='error_func_view'),
]
