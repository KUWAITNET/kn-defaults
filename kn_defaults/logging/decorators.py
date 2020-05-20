import sys
from functools import wraps
import logging

logger = logging.getLogger('kn_defaults')
from django.utils.decorators import method_decorator


def log_activity(verb, target=None, level=0):
    def decorator(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            obj = func(self, *args, **kwargs)
            # if hasattr(self, 'txn_type'):
            #     # means the object is PaymentTransaction
            #     # get the verbose name of it.
            #     msg = f'{verb} ' \
            #         f'{next(f[1] for f in constants.TYPE_CHOICES if f[0] == self.txn_type)}'
            # else:
            msg = verb

            params = {'verb': msg}

            if callable(target):
                params['target'] = target(obj)

            # sometimes target object is passed in, because action_object doesn't exist,
            # ie: it was deleted
            # in that case, obj returned by the function is the target obj
            if obj is not None and params.get('target') != obj:
                params['action_object'] = obj

            logger.log(level, f'{params["verb"]} - f{params["target"]}', exc_info=sys.exec_info, extra={
                'request': self.request,
                'status_code': obj.status_code
            })
            # action.send(self.request.user, **params)

            return obj

        return inner

    return decorator


