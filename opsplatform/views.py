import logging
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


LOGGER = logging.getLogger('__name__')


def index(request):
    LOGGER.info("start application")
    LOGGER.error("fail to start application")
    return redirect('/website/')


@login_required()
def noperm(request):
    return render(request, 'noperm.html', {"user": request.user})