import re
from pyproj import Proj, transform

IS_CLOSED_KEYWORDS = ["library", "caf", "centre", "bar", "brasserie", "public house", "pub", "room", "house", "the",
                      "club", "centre", "restaurant", "court", "coffee", "tea", "kebab", "curry", "hall", "hair"]
DISABLED_KEYWORDS = ["accessible", "disabled", "wheelchair", "access"]
BABY_CHANGE_KEYWORDS = ["baby", "babychange", "change", "changing", "baby change"]
OPENING_HOURS_KEYWORDS = ["mon", "tue", "wed", "thur", "fri", "sat", "sun", "holidays", ":00", "00", "24hr"]
NOT_ADDRESS_KEYWORDS = ["yes", "no", "available", "only", "free"]
IS_FEE_KEYWORDS = ["20p", "pound", "free", "50p", "75p", "paid"]

# some clever AI to detect what a piece of text is related to : )


def is_related_to_babychange(text):
    for w in BABY_CHANGE_KEYWORDS:
        if w in text.lower():
            return True
    return False


def is_related_to_disabled(text):
    for w in DISABLED_KEYWORDS:
        if w in text.lower():
            return True
    return False


def is_related_to_opening(text):
    for w in OPENING_HOURS_KEYWORDS:
        if w in text.lower():
            return True
    return False


def is_probably_closed_covid(text):
    for w in IS_CLOSED_KEYWORDS:
        if w in text.lower():
            return True
    return False


def is_probably_fee_related(text):
    for w in IS_FEE_KEYWORDS:
        if w in text.lower():
            return True
    return False


def is_probably_an_address(text):
    for w in OPENING_HOURS_KEYWORDS + DISABLED_KEYWORDS + BABY_CHANGE_KEYWORDS + NOT_ADDRESS_KEYWORDS + IS_FEE_KEYWORDS:
        if w in text.lower():
            return False
    return True


def split_text_with_any_possible_delimiter(text):
    return re.split(r';|,|\.|<br>|<br/>', text)


# data cleaning

def cleanxml(raw_xml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_xml)
    return cleantext


def only_single_whitespace(s):
    return " ".join([p for p in s.split() if p != ""])


def remove_all_whitespace(str):
    return str.replace(" ", "")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple - unintuitive order"""
    v84 = Proj(proj="latlong", towgs84="0,0,0", ellps="WGS84")
    v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy",
               towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894")
    vgrid = Proj(init="world:bng")
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)
