from rest_framework import permissions

class IsGroupOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if obj in request.user.extension.groups.all():
                    return True
            except BaseException:
                return False
                raise
        return False

class IsAssetOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if obj in request.user.extension.getassets():
                    return True
            except BaseException:
                return False
                raise
        return False

class IsSoftwareOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if obj in request.user.extension.getsoftwares():
                    return True
            except BaseException:
                return False
                raise
        return False

class IsVulnerabilityOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if obj in request.user.extension.getvulnerabilities():
                    return True
            except BaseException:
                return False
                raise
        return False