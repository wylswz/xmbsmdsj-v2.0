from patent.settings import MEDIA_URL


def processor(request):
    return {"media_url": MEDIA_URL }