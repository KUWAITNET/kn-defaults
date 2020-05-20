from django.http import HttpResponse
from django.urls import path


def success_func_view(request):
    return HttpResponse(content='Ok')


urlpatterns = [
    path('', success_func_view, name='success_func_view'),
    # path('', ra_admin_site.urls),
]
