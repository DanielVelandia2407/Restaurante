from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.waiter.charge == 'MG'

class IsManagerOrAdminTables(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.waiter.charge in ['MG', 'AT']