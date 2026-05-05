from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        user = None
        try:
            # Try to get user by username, email, or first_name (display name)
            user = User.objects.filter(
                Q(username__iexact=username) | 
                Q(email__iexact=username) | 
                Q(first_name__iexact=username)
            ).first()
        except Exception:
            return None
        
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
