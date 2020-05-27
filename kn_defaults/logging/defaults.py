KN_FORMATTER = "%(levelname)s:%(name)s; " \
               "REQ_id:%(request_id)s; %(message)s; path=%(path)s; method=%(method)s;ip=%(ip)s; " \
               "status_code:%(status_code)%; response_duration:%(response_duration)s; " \
               "post_parameters: %(post_parameters)s; outbound:%(outbound_payload)s"
KN_FORMATTER = "{levelname} {name}; {message} {outbound_payload}"
BASE_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose_kn': {
            'format': KN_FORMATTER,
        },
    },
    'handlers': {
        'kn_default_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose_kn'
        },
    },
    'loggers': {
        'kn_defaults': {
            'handlers': ['kn_default_handler'],
            'level': 'INFO',
        }
    }
}
