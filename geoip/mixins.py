import os
import pygeoip

BASE_DIR = os.path.dirname(__file__)


class GeoIpMixin(object):
    gi = pygeoip.GeoIP(os.path.join(BASE_DIR, 'GeoIP.dat'))

    def ip_lookup(self, ip):
        code = self.gi.country_code_by_addr(ip).lower()
        if not code:
            return ['unknown', 'Unknown']
        return [self.gi.country_code_by_addr(ip).lower(),
                self.gi.country_name_by_addr(ip)]