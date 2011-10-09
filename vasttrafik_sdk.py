import simplejson as json
import urllib
import logging

base_url = 'http://api.vasttrafik.se/bin/rest.exe/'
version = 'v1'
format = 'json'
jsonp_callback = ''
vt_api_key = '' # Your developer key

class vast_trafik(object):
    def __init__(self, app_key):
        self.prefix = '%s%s/' % (base_url, version)
        self.general_params = dict(
                        authKey         = app_key,
                        format          = format, 
                        jsonpCallback   = jsonp_callback
                        )
        
    def trip(self, origin_lat=None, origin_lon=None, origin_name=None, \
        origin_id=None, dest_lat=None, dest_lon=None, dest_name=None, \
        dest_id=None, date = None, time = None, search_for_arrival = 0, \
        num_trips=5):
        if (not origin_id) and (not dest_id):
            params = dict(
                originCoordLat      = origin_lat,
                originCoordLong     = origin_lon,
                originCoordName     = origin_name,
                destCoordLat        = dest_lat,
                destCoordLong       = dest_lon,
                destCoordName       = dest_name,
                date                = date,
                time                = time,
                searchForArrival    = search_for_arrival,
                numTrips            = num_trips)
            params.update(self.general_params)
            url = self.prefix + u'trip'
            url = '%s?%s' % (url, urllib.urlencode(params))
            logging.info('fetching [%s]...' % url)
            return self.get_json(url)
                        
    def near_by_stops(self, origin_lat=None, origin_lon=None, max_no=30):
        if origin_lat and origin_lon:
            params = dict(
                originCoordLat  = origin_lat, 
                originCoordLong = origin_lon,
                maxNo           = max_no)
            params.update(self.general_params)
            url = '%s%s?%s' % (self.prefix, u'location.nearbystops', urllib.urlencode(params))
            logging.info('fetching [%s]...' % url)
            return self.get_json(url)
        else:
            return None
            
    def get_json(self, url):
        response = (urllib.urlopen(url).read())
        try:
            data = json.loads(response[1:-2])
        except:
            return None
        else:
            return data
