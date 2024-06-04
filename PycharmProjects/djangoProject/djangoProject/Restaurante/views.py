from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from .models import (
    Restaurant, Table, TablesRestaurant, Product, ProductsRestaurant, Waiter,
    Order, ProductsOrder, Bill, TipWaiter, WaiterShift, User
)
from .serializers import (
    RestaurantSerializer, TableSerializer, TablesRestaurantSerializer, ProductSerializer,
    ProductsRestaurantSerializer, WaiterSerializer, OrderSerializer, ProductsOrderSerializer,
    BillSerializer, TipWaiterSerializer, WaiterShiftSerializer, UserSerializer
)
from .permissions import IsManager, IsManagerOrAdminTables

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=False, methods=['get'])
    def por_mesero(self, request):
        mesero_id = request.query_params.get('mesero_id')
        if (mesero_id):
            current_shifts = WaiterShift.objects.filter(
                waiter_id=mesero_id,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
            mesas = Table.objects.filter(tablesrestaurant__restaurant__waitershift__in=current_shifts)
        else:
            mesas = Table.objects.none()
        serializer = self.get_serializer(mesas, many=True)
        return Response(serializer.data)

class TablesRestaurantViewSet(viewsets.ModelViewSet):
    queryset = TablesRestaurant.objects.all()
    serializer_class = TablesRestaurantSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductsRestaurantViewSet(viewsets.ModelViewSet):
    queryset = ProductsRestaurant.objects.all()
    serializer_class = ProductsRestaurantSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        if not IsManagerOrAdminTables().has_permission(request, self):
            return Response({'detail': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def por_mesero(self, request, pk=None):
        waiter = Waiter.objects.get(pk=pk)
        active = request.query_params.get('active')
        if active:
            ordenes = Order.objects.filter(waiter=waiter, bill__isnull=True)
        else:
            ordenes = Order.objects.filter(waiter=waiter)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)

class ProductsOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductsOrder.objects.all()
    serializer_class = ProductsOrderSerializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def destroy(self, request, *args, **kwargs):
        if not IsManager().has_permission(request, self):
            return Response({'detail': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def generar_cuenta(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        bill, created = Bill.objects.get_or_create(order=order)
        if created:
            bill.cost = order.productorder_set.aggregate(total=Sum('product__cost_per_unit'))['total']
            bill.save()
        serializer = self.get_serializer(bill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TipWaiterViewSet(viewsets.ModelViewSet):
    queryset = TipWaiter.objects.all()
    serializer_class = TipWaiterSerializer

class WaiterViewSet(viewsets.ModelViewSet):
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer

    @action(detail=True, methods=['get'])
    def get_tips(self, request, pk=None):
        waiter = self.get_object()

        paid_tips = TipWaiter.objects.filter(waiter=waiter, paid=True).aggregate(total=Sum('bill__tip_percent'))[
                        'total'] or 0
        unpaid_tips = TipWaiter.objects.filter(waiter=waiter, paid=False).aggregate(total=Sum('bill__tip_percent'))[
                          'total'] or 0

        response_data = {
            'tips_payed': paid_tips,
            'current_tips': unpaid_tips
        }

        return Response(response_data)

    @action(detail=True, methods=['post'])
    def add_shift(self, request, pk=None):
        waiter = self.get_object()
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        restaurant_id = request.data.get('restaurant')

        shift = WaiterShift.objects.create(
            waiter=waiter,
            start_date=start_date,
            end_date=end_date,
            restaurant_id=restaurant_id
        )
        return Response({'status': 'shift added'}, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WaiterShiftViewSet(viewsets.ModelViewSet):
    queryset = WaiterShift.objects.all()
    serializer_class = WaiterShiftSerializer
