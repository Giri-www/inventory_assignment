from django.db import models
from django.contrib.auth.models import User
from inventory.models import AuditTimestampModel

class UserDetails(AuditTimestampModel):
    ''' User Details Model '''
    user_details_id = models.BigAutoField("userdetailsId", primary_key=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, help_text="User Id"
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        ''' Meta Class '''
        db_table = 'user_details'