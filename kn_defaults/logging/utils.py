import time

CLEANSED_SUBSTITUTE = '********************'


def get_data(request, exception=None):
    data = dict(
        request_id=request.kn_default_log_id,
        method=request.method,
        path=request.path[:255],
        ip=request.META.get('REMOTE_ADDR', ''),
        user=request.user if request.user.is_authenticated else None,
        post_parameters=get_post_parameters(request, request.method)
    )
    return data


def get_post_parameters(request, method='POST'):
    """
    Copy of `django/views/debug.py SafeExceptionReporterFilter.get_post_parameters
    Replace the values of POST parameters marked as sensitive with
    stars (*********).
    """
    if request is None:
        return {}
    else:
        sensitive_post_parameters = getattr(request, 'sensitive_post_parameters', [])
        cleansed = getattr(request, method).copy()
        if sensitive_post_parameters:
            if sensitive_post_parameters == '__ALL__':
                # Cleanse all parameters.
                for k in cleansed:
                    cleansed[k] = CLEANSED_SUBSTITUTE
                return cleansed
            else:
                # Cleanse only the specified parameters.
                for param in sensitive_post_parameters:
                    if param in cleansed:
                        cleansed[param] = CLEANSED_SUBSTITUTE
                return cleansed
        else:
            return cleansed


def log(request, level, msg, args, exc_info=None, extra=None, stack_info=False):
    data = get_data
