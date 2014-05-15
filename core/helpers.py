import datetime
import warnings

from functools import wraps
from django.core.cache import cache
from django.db import connection
from django.utils.encoding import iri_to_uri


def cache_cbv_method_until_midnight(method):
    """
    Caches a CBV (class based view) method until local midnight
    Used for calculations that don't use today's data (e.g. monthly chart)

    Cache key is built from module name, method name and request path
    """

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        key = '{0}.{1}():{2}'.format(method.__module__, method.__name__, iri_to_uri(self.request.get_full_path()))
        seconds = self.seconds_until_midnight()

        result = cache.get(key)
        if result is None:
            # key not in cache, call actual method and add to cache
            result = method(self, *args, **kwargs)
            cache.set(key, result, seconds)

        return result

    return wrapped


def timezone_offset(tz):
    delta_offset = tz.utcoffset(datetime.datetime.now())
    hours = delta_offset.days * 24
    hours += delta_offset.seconds // 3600
    return '{0}:00'.format(hours)


def get_date_truncate(truncate, fieldname, timezone):
    if connection.vendor != 'postgresql':
        warnings.warn('Not running on PostgreSQL, timezone support not entirely functional on other backends yet. '
                      'Falling back to no-timezone mode in some calculations.')
        return connection.ops.date_trunc_sql(truncate, fieldname)
    return "DATE_TRUNC('{0}', {1} AT TIME ZONE INTERVAL '{2}')".format(truncate, fieldname, timezone_offset(timezone))
