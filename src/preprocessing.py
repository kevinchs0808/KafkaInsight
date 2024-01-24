import parameters

def reformat_time(text):
    text = text[1:]
    text_components = text.split(":")
    date = text_components[0]
    time = ":".join(text_components[1:])

    date_components = date.split("/")
    date = "-".join([date_components[2], parameters.month_mapping[date_components[1]], date_components[0]])

    datetime = date + " " + time

    return datetime

def find_timezone(text):
    text = text[:-1]
    mode = text[0]
    hour = int(text[1:3]) + round(int(text[3:])/parameters.hour_in_minutes, parameters.decimal_rounding)
    return "GMT"+mode+str(hour)


def simplify_status(status_code):
    return parameters.status_mapping[status_code[0]]


def user_detection(name):
    if name == "-":
        return "Anonymous"
    else:
        return "User Exists"