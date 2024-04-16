import geocoder

class LocationManager:
    def __init__(self):
        pass  

    def get_location(self, manual_location=None):
        """Fetches the user's location via IP address or uses a provided manual location."""
        try:
            if manual_location:
                return manual_location.split(', ')[-1]  
            else:
                g = geocoder.ip('me')
                return g.country if g.country else 'Default Country'
        except Exception as e:
            print(f"Failed to get location: {e}")
            return 'Default Country'