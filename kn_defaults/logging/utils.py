from django.conf import settings
from django.urls import get_resolver, get_urlconf, NoReverseMatch, reverse
from django.utils.translation import get_language


class PatternsAnalyzer:
    def __init__(self, patterns):
        self.patterns = patterns
        self.paths_dicts = self.parse_patterns(patterns)

    def parse_patterns(self, patterns):
        """
        Validate Patterns
        :param patterns: a list of patterns
        :return:
        """
        errors = []

        urlconf = get_urlconf()
        resolver = get_resolver(urlconf)
        included_urls = []

        paths_dict = {}
        for pattern in patterns:
            exclude = False

            if pattern.startswith('-'):
                exclude = True
                pattern = pattern[1:]

            if pattern == '*':
                # we log everything
                path = '*'

            elif ':*' in pattern:
                # validate namespace actually exists
                namespace = pattern.split(':')[0]

                namespace_resolver = resolver.namespace_dict.get(namespace, False)
                if not namespace_resolver:
                    errors.append(f'{namespace} namespace does not exists')
                    raise

                path = self.remove_language_prefix(namespace_resolver[0])
                sub_paths = namespace_resolver.url_patterns

            else:
                # that's a normal pattern
                try:
                    path = reverse(pattern)
                except NoReverseMatch:
                    errors.append(f'{pattern} pattern does not exists')
                    raise

            paths_dict[path] = {
                'exclude': exclude
            }

    def remove_language_prefix(self, pattern):
        """
        Remove the language prefix
        Example: remove_language_prefix('ar/some-url/') -> 'some-url/'
        :param pattern:
        :return:
        """
        language_code = get_language() or settings.LANGUAGE_CODE
        if pattern.startswith(language_code):
            pattern = pattern.replace(f'{language_code}/', '')
        return pattern

    def shall_log(self, url_path):
        # check if it's excluded first then check if it's included.
        url_path = self.remove_language_prefix(url_path)
        log_all = self.paths_dicts.get('*', False)

        for path, v in self.paths_dicts.items:
            if path == url_path and v['excluded']:
                # the path is definitely excluded
                return False
            # elif



