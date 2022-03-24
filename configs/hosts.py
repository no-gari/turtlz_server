from django_hosts import patterns, host


host_patterns = patterns(
    host('', 'configs.urls', name='api'),
)
