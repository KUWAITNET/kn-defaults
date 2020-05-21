import pdb
import sys
import time
import traceback
import simplejson as json
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger('kn_defaults')


class KnLogging(MiddlewareMixin):
    """
    In charge of logging events and speed of views, names urls specified in sewttings

    """

    @staticmethod
    def shall_log(request, namespace=None, url_name=None):
        from . import app_settings
        resolver = resolve(request.path)
        namespace = resolver.namespace
        url_name = resolver.view_name

        patterns = app_settings.KN_LOGGING_URL_PATTERNS
        # pdb.set_trace()
        check_url_name = f'{namespace}:{url_name}' if namespace else url_name
        if check_url_name in patterns:
            return True
        elif f'{namespace}:*' in patterns:
            return True
        return False

    def __init__(self, get_response=None):
        self.get_response = get_response
        from .app_settings import KN_LOGGING_URL_PATTERNS
        self.patterns = KN_LOGGING_URL_PATTERNS
        self.start = None
        super(KnLogging, self).__init__(get_response)
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.start = time.time()
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        if self.shall_log(request):
            # if True:
            # Request info
            method = request.method
            path = request.path[:255]
            ip = request.META.get('REMOTE_ADDR', '')
            user = request.user if request.user.is_authenticated else None
            status_code = response.status_code
            outbound_payload = ''
            response_duration = time.time() - self.start

            try:
                outbound_payload = json.loads(response.content)
            except:
                pass

            if response.status_code in [200, 301, 302]:
                logger.info(f'{request.path} took {response_duration} seconds, response: {response.status_code}')
            # elif response.status_code == 500:

        return response

    def process_exception(self, request, exception):
        traceback_ = traceback.format_exc()
        logger.error(f'Internal server error Path f{request.path}, Trace{traceback_}', exc_info=sys.exc_info())
