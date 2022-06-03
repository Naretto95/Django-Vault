from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Vulnerability(TimeStampMixin):
    name = models.CharField(max_length=100,verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    cpe = models.ForeignKey('CPE', on_delete=models.CASCADE,verbose_name=_('CPE'), related_name='+')
    slug = AutoSlugField(_('Slug'), unique=True, max_length=100, populate_from=('name','cpe'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Vulnerability,self).save(*args, **kwargs)
        self.cpe.vulnerabilities.add(self)

class CPE(TimeStampMixin):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    reference = models.TextField(verbose_name=_('Reference'))
    vulnerabilities = models.ManyToManyField(Vulnerability, blank=True, verbose_name=_('Vulnerabilities'), related_name='+')

    def __str__(self):
        return self.name

class Software(TimeStampMixin):
    name = models.CharField(max_length=100,verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    version = models.CharField(max_length=100,verbose_name=_('Version'))
    cpe = models.ForeignKey('CPE', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('CPE'))
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE,verbose_name=_('Asset'), related_name='+')
    slug = AutoSlugField(_('Slug'), unique=True, max_length=100, populate_from=('name','version','asset'))

    def __str__(self):
        return self.name

    def getvulnerabilities(self):
        return self.cpe.vulnerabilities.all()

    def save(self, *args, **kwargs):
        super(Software,self).save(*args, **kwargs)
        self.asset.softwares.add(self)

class Asset(TimeStampMixin):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    group = models.ForeignKey('Group', on_delete=models.CASCADE,verbose_name=_('Group'), related_name='+')
    description = models.TextField(verbose_name=_('Description'))
    softwares = models.ManyToManyField(Software, blank=True, verbose_name=_('Softwares'), related_name='+')
    slug = AutoSlugField(_('Slug'), unique=True, max_length=100, populate_from=('name','group'))

    def getvulnerabilities(self):
        return Vulnerability.objects.filter(cpe__in=self.softwares.values_list('cpe',flat=True))

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Asset,self).save(*args, **kwargs)
        self.group.assets.add(self)

class Group(TimeStampMixin):
    extension = models.ForeignKey('Extension', on_delete=models.CASCADE,verbose_name=_('Extension'), related_name='+')
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    assets = models.ManyToManyField(Asset, blank=True, verbose_name=_('Assets'), related_name='+')
    slug = AutoSlugField(_('Slug'), unique=True, max_length=100, populate_from=('name'))

    def getsoftwares(self):
        return Software.objects.filter(asset__in=self.assets.all())
    
    def getvulnerabilities(self):
        return Vulnerability.filter(cpe__in=self.getsoftwares().values_list('cpe',flat=True))
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Group,self).save(*args, **kwargs)
        self.extension.groups.add(self)

class Extension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('Group(s)'), related_name='+')

    @receiver(post_save, sender=User)
    def create_user_extension(sender, instance, created, **kwargs):
        if created:
            Extension.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_extension(sender, instance, **kwargs):
        instance.extension.save()

    def getassets(self):
        return Asset.objects.filter(group__in=self.groups.all())

    def getsoftwares(self):
        return Software.objects.filter(asset__in=self.getassets())
    
    def getvulnerabilities(self):
        return Vulnerability.objects.filter(cpe__in=self.getsoftwares().values_list('cpe',flat=True))

    def __str__(self):
        return self.user.username
    