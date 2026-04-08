from django.db import models
from accounts.models import AuthUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from uuid import uuid4
from pathlib import Path



    
class VulnerType(models.TextChoices):
    XSS = "XSS", "XSS"
    SQLI = "SQLI", "SQLI"
    RCE = "RCE", "RCE"
    IDOR = "IDOR", "IDOR"
    CSRF = "CSRF", "CSRF"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION", "Privilege Escalation"
    BUSINESS_LOGIC = "BUSINESS_LOGIC", "Business Logic"
    SUBDOMAIN_TAKES_OVER = "SUBDOMAIN_TAKES_OVER", "Subdomain Takes Over"
    HOST_HEADER_INJECTION = 'HOST_HEADER_INJECTION', "Host Header Injection"


class Severity(models.IntegerChoices):
    LOW = 0, "Low"
    MEDIUM = 1, "Medium"
    HIGH = 2, "High"
    CRITICAL = 3, "Critical"





class VulnerStatus(models.TextChoices):
    NEW = 'NEW', 'New'
    UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
    RESOLVED = "RESOLVED", 'Resolved'
    DUPLICATED = "DUPLICATED", 'Duplicated'
    INFORMATIVE = 'INFORMATIVE', 'Informative'
    OUT_SCOPE = 'OUT_OF_SCOPE', "Out Of Scope"



class Report(models.Model):
    user = models.ForeignKey(
        to=AuthUser,
        on_delete=models.SET_NULL,
        related_name='reports',
        verbose_name='User',
        null=True,
        blank=True
    )




    title = models.CharField(max_length=250, verbose_name='Title')
    vulner_type = models.CharField(max_length=100, choices=VulnerType.choices, verbose_name='Type', db_index=True)
    severity = models.SmallIntegerField(choices=Severity.choices, verbose_name='Serverity', db_index=True, validators=[MinValueValidator(0), MaxValueValidator(3)])
    url = models.URLField(verbose_name='Url')
    description = models.TextField(verbose_name='Description')
    steps_to_reproduce = models.TextField(verbose_name='Steps To Reproduce')
    poc = models.FileField(verbose_name='Proof Of Concept', upload_to='vdp/%Y-%m-%d', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'png', 'jpg', 'jpeg', 'mov'])])
    impact = models.TextField(verbose_name='Impact')
    recommended_fix = models.TextField(verbose_name='Recommended Fix', blank=True, null=True)
    status = models.CharField(max_length=30, verbose_name='Status', choices=VulnerStatus.choices, default=VulnerStatus.NEW, db_index=True)
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated At', auto_now=True)

    class Meta:
        ordering = ['-created_at']




    def save(self, *args, **kwargs):
        if not self.pk:
            extension_file = Path(self.poc.name).suffix
            self.poc.name = f'{uuid4()}{extension_file}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} | {self.vulner_type}'
    