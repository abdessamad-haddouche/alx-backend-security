from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import RequestLog
import logging

logger = logging.getLogger(__name__)

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Log the IP address, timestamp, and path of every incoming request.
        """
        try:
            # Get the client IP address
            ip_address = self.get_client_ip(request)
            
            # Get the request path
            path = request.get_full_path()
            
            # Log the request
            RequestLog.objects.create(
                ip_address=ip_address,
                timestamp=timezone.now(),
                path=path
            )
            
        except Exception as e:
            # Log the error but don't break the request
            logger.error(f"Error logging request: {e}")
        
        return None
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        Handles cases where the request comes through proxies.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip