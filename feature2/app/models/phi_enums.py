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
