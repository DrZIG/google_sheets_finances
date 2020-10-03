from enum import Enum


class HorizontalAlignment(str, Enum):
    """
    according to https://developers.google.com/apps-script/reference/document/horizontal-alignment
    """

    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'
    JUSTIFY = 'JUSTIFY'


class VerticalAlignment(str, Enum):
    """
    according to https://developers.google.com/apps-script/reference/document/vertical-alignment
    """

    BOTTOM = 'BOTTOM'
    CENTER = 'MIDDLE'  # according to https://stackoverflow.com/a/39214709/9712980 CENTER → MIDDLE
    TOP = 'TOP'
