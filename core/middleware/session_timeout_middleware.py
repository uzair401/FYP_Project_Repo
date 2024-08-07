# myapp/middleware.py
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect
from datetime import timedelta, datetime

class SessionTimeoutMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.session.get('last_activity') is None:
                request.session['last_activity'] = datetime.now().timestamp()
            elif (datetime.fromtimestamp(request.session.get('last_activity')) + timedelta(minutes=10)) < datetime.now():
                request.session.flush()
                return HttpResponseRedirect('/login/')
            request.session['last_activity'] = datetime.now().timestamp()
        return None