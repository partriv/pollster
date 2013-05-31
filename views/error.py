from pollster.consts import consts
from pollster.views.base import base

def index(request):
    error_code = int(request.GET['error'])

    try:
        error = consts.ERROR_ENGLISH[error_code]
    except:
        error = 'Unknown error.'
    return base.render(request, "error.html", {"error":error,})
