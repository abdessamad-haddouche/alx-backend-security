from django.db import models
from django.utils import timezone

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'ip_tracking_requestlog'
        ordering = ['-timestamp']
    
    def __str__(self):
        location = f"{self.city}, {self.country}" if self.city and self.country else "Unknown"
        return f"{self.ip_address} ({location}) - {self.path} - {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'ip_tracking_blockedip'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Blocked IP: {self.ip_address}"