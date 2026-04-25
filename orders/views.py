from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from store.models import Cart
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            cart = get_object_or_404(Cart, user=request.user)
            if not cart.items.exists():
                return Response({'error': 'Cart is empty'}, status=400)
            total = 0
            cart_items = cart.items.select_related('product').all()
            for item in cart_items:
                if item.quantity > item.product.stock:
                    return Response({'error': f'Insufficient stock for {item.product.name}'}, status=400)
            order = Order.objects.create(
                user=request.user,
                full_name=serializer.validated_data['full_name'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data['phone'],
                address=serializer.validated_data['address'],
                payment_method=serializer.validated_data['payment_method'],
                payment_status='pending',
                order_status='pending',
                total_amount=0,
            )
            for item in cart_items:
                subtotal = item.product.price * item.quantity
                total += subtotal
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    subtotal=subtotal,
                )
            order.total_amount = total
            order.save()
            cart.items.all().delete()
            return Response({
                'message': 'Order placed successfully',
                'order': OrderSerializer(order).data,
                'note': 'Offline payment selected. Admin will confirm payment before processing.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
