from django.db import models

# Create your models here.
''' AuditTimestamp Models '''
class AuditTimestampModel(models.Model):
    created_by = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ''' Meta Class '''
        abstract = True


class Item(AuditTimestampModel):
    models.BigAutoField("Id", primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
