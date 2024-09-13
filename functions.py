from datetime import datetime, timedelta


def time_cleaner(time):

    if "ساعت پیش" in time:
        time = int(time.replace("ساعت پیش", "").strip())
        return datetime.now() - timedelta(hours=time)

    elif "دقیقه پیش" in time:
        time = int(time.replace("دقیقه پیش", "").strip())
        return datetime.now() - timedelta(minutes=time)

    elif "روز پیش" in time:
        time = int(time.replace("روز پیش", "").strip())
        return datetime.now() - timedelta(days=time)

    elif "ثانیه پیش" in time:
        time = int(time.replace("ثانیه پیش", "").strip())
        return datetime.now() - timedelta(seconds=time)

    return datetime.now()


def title_cleaner(title):
    return title.replace(r"\u200c", " ")

