from geopy.geocoders import Nominatim

locator = Nominatim(user_agent='test')


def address_to_gps(adresse):
    location = locator.geocode(adresse)
    return location.latitude, location.longitude


def correct_address(adresse):
    location = locator.geocode(adresse)
    return location.address
