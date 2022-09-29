import enum


class DataType(enum.Enum):
    sleep = 'sleep'
    hr = 'hr'
    steps = 'steps'
    detailed = 'detailed'
    summary = 'summary'
    ema = 'ema'
    isi = 'isi'
    sleep_diary = 'sleep_diary'
    activities = 'activities'
    ema_morning = 'ema_morning'
    ema_evening = 'ema_evening'
    nb = 'nb'


class SourceType(enum.Enum):
    fitbit = 'fitbit'
    withings = 'withings'
    app = 'app'


class QCStatus(enum.Enum):
    FAILURE = -1
    EMPTY = 0
    SUCCESS = 1
    WARNING = 2


class Hand(enum.Enum):
    LEFT = 0
    RIGHT = 1


class BedSharedWith(enum.Enum):
    ALONE = 0
    PET = 1
    PERSON = 2
    PET_AND_PERSON = 3


class Sex(enum.Enum):
    MALE = 0
    FEMALE = 1


class KitStatus(enum.Enum):
    waiting_for_cvb_shipment = 'waiting_for_cvb_shipment'
    in_transit_to_shipper = 'in_transit_to_shipper'
    delivered_to_shipper = 'delivered_to_shipper'
    waiting_for_subject = 'waiting_for_subject'
    assigned_to_subject = 'assigned_to_subject'
    in_transit_to_subject = 'in_transit_to_subject'
    delivered_to_subject = 'delivered_to_subject'
    received_by_subject = 'received_by_subject'
    devices_set_up = 'devices_set_up'
    recording_complete = 'recording_complete'
    in_transit_back_to_shipper = 'in_transit_back_to_shipper'
    delivered_back_to_shipper = 'delivered_back_to_shipper'
    released_from_subject = 'released_from_subject'
    in_transit_back_to_cvb = 'in_transit_back_to_cvb'
    delivered_to_cvb = 'delivered_to_cvb'
    received_by_cvb = 'received_by_cvb'
    in_batch = 'in_batch'


class TypeTimeZone(enum.Enum):
    EASTERN_TZ = "US/Eastern"
    CENTRAL_TZ = "US/Central"
    MOUNTAIN_TZ = "US/Mountain"
    PACIFIC_TZ = "US/Pacific"
