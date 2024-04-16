from datetime import datetime

base_url = 'https://api.energy-charts.info/'
country_code = 'ch'

def process_timestamps(unix_seconds):
    """ Convert list of unix timestamps to datetime objects. """
    return [datetime.utcfromtimestamp(ts) for ts in unix_seconds]
