from rest_framework import serializers
from .models import *

class SerialMixin(serializers.HyperlinkedModelSerializer):
    vulnerabilities_count = serializers.SerializerMethodField()
    softwares_count = serializers.SerializerMethodField()
    assets_count = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_vulnerabilities_count(self, obj):
        return obj.getvulnerabilities().count()

class GroupSerializer(SerialMixin):
    assets_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id','name','description','vulnerabilities_count','assets_count','slug')

    def get_assets_count(self, obj):
        return obj.assets.all().count()

class AssetSerializer(SerialMixin):
    
    class Meta:
        model = Asset
        fields = ('id','name','description','vulnerabilities_count','softwares_count','slug')

    def get_softwares_count(self, obj):
        return obj.softwares.all().count()

class SoftwareSerializer(SerialMixin):
    cpe = serializers.SlugRelatedField(queryset=CPE.objects.all(),many=False, slug_field="name")

    class Meta:
        model = Software
        fields = ('id','name','description','version','cpe','vulnerabilities_count','slug')

class VulnerabilitySerializer(serializers.HyperlinkedModelSerializer):
    cpe = serializers.SlugRelatedField(queryset=CPE.objects.all(),many=False, slug_field="name")

    class Meta:
        model = Vulnerability
        fields = ('id','name','description','score','severity','link','cpe','slug')