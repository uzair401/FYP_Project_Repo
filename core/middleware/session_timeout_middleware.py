from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime, timedelta

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            now = datetime.now()
            last_activity = request.session.get('last_activity', now.timestamp())

            if (datetime.fromtimestamp(last_activity) + timedelta(minutes=10)) < now:
                # Session has timed out
                print('Logout and Session Flush is initiated')
                logout(request)  # Log out the user
                request.session.flush()  # Clear the session
                return redirect('/login/')  # Redirect to login page

            # Update last activity time
            request.session['last_activity'] = now.timestamp()
        return None
