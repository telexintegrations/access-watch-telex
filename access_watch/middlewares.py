from django.core.cache import cache
import re
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class AccessMonitoringMiddleware:

    def __init__(self, get_response):
        self.SECURED_ENDPOINT = r"^/api/v1/secured-data/?$"
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed before the view is called.
        self.process_request(request)

        response = self.get_response(request)

        # Code to be executed after the view is called.
        return response

    def process_request(self, request):
        """Monitor access attempts to secured endpoints."""
        path = request.path

        # Check if the request matches the secured endpoint
        if not re.match(self.SECURED_ENDPOINT, path):
            return

        ip_address = self.get_client_ip(request)
        user = self.get_authenticated_user(request)

        if user is None:
            # Track anonymous user access
            cache_key = f"anon_access_{ip_address}"
            access_count = cache.get(cache_key, 0) + 1
            cache.set(cache_key, access_count, timeout=86400)  # Store for a day
            self.track_cache_key(cache_key)  # Track the key

        elif not user.is_staff:  # If the user is authenticated but lacks admin rights
            cache_key = f"user_access_{user.username}"
            access_count = cache.get(cache_key, 0) + 1
            cache.set(cache_key, access_count, timeout=86400)  # Store for a day
            self.track_cache_key(cache_key)  # Track the key

    def track_cache_key(self, key):
        """Store a reference of the key in a cache list."""
        keys_list = cache.get("cached_keys", set())  # Get existing keys
        keys_list.add(key)
        cache.set("cached_keys", keys_list, timeout=86400)  # Store for a day

    def get_authenticated_user(self, request):
        """Manually authenticate the user using JWT."""
        try:
            auth = JWTAuthentication()
            user, _ = auth.authenticate(request)
            return user
        except AuthenticationFailed:
            return None
        except TypeError:
            return None

    def get_client_ip(self, request):
        """Extract the IP address of the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_all_cached_access_data():
        """Retrieve all stored access attempts."""
        keys_list = cache.get("cached_keys", set())  # Retrieve stored keys
        return {key: cache.get(key) for key in keys_list}
