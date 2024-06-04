from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Restaurante.views import (
    RestaurantViewSet, TableViewSet, TablesRestaurantViewSet, ProductViewSet,
    ProductsRestaurantViewSet, WaiterViewSet, OrderViewSet, ProductsOrderViewSet,
    BillViewSet, TipWaiterViewSet, WaiterShiftViewSet, UserViewSet
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurante",
        default_version='v1',
        description="Proyecto de ejemplo para el curso de Django",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dfvelandiaj@udistrital.edu.co"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'tables', TableViewSet)
router.register(r'tables-restaurants', TablesRestaurantViewSet)
router.register(r'products', ProductViewSet)
router.register(r'products-restaurants', ProductsRestaurantViewSet)
router.register(r'waiters', WaiterViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'products-orders', ProductsOrderViewSet)
router.register(r'bills', BillViewSet)
router.register(r'tip-waiters', TipWaiterViewSet)
router.register(r'waiter-shifts', WaiterShiftViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]