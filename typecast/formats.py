
def create_date_formats():
    """ Generate combinations of time and date formats with different
    delimeters. """
    # European style:
    base_formats = ['%d %m %Y', '%d %m %y', '%Y %m %d']
    # US style:
    base_formats += ['%m %d %Y', '%m %d %y', '%Y %m %d']
    # Things with words in
    base_formats += ['%d %b %Y', '%d %B %Y']

    date_formats = []
    for separator in ('-', '.', '/', ' '):
        for date_format in base_formats:
            date_formats.append((date_format.replace(' ', separator)))

    datetime_formats = []
    time_formats = ('%H:%M%Z', '%H:%M:%S', '%H:%M:%S%Z', '%H:%M%z',
                    '%H:%M:%S%z')

    for date_format in date_formats:
        for time_format in time_formats:
            for separator in ('', 'T', ' '):
                datetime_formats.append(date_format + separator + time_format)

    return tuple(date_formats), tuple(datetime_formats)


DATE_FORMATS, DATETIME_FORMATS = create_date_formats()
