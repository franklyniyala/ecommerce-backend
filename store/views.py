from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Category, Product, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, AddToCartSerializer, UpdateCartItemSerializer

class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)

class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category')
        search = request.query_params.get('search')
        queryset = Product.objects.filter(is_active=True)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search:
            queryset = queryset.filter(name__icontains=search)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        serializer = CartSerializer(self.get_cart(request.user))
        return Response(serializer.data)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Product, id=serializer.validated_data['product_id'], is_active=True)
            quantity = serializer.validated_data['quantity']
            if quantity > product.stock:
                return Response({'error': 'Requested quantity exceeds available stock'}, status=400)
            cart = self.get_cart(request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock:
                    return Response({'error': 'Total cart quantity exceeds available stock'}, status=400)
                cart_item.quantity = new_quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return Response({'message': 'Item added to cart'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            quantity = serializer.validated_data['quantity']
            if quantity > cart_item.product.stock:
                return Response({'error': 'Requested quantity exceeds available stock'}, status=400)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'message': 'Cart item updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'Cart item removed successfully'}, status=status.HTTP_204_NO_CONTENT)
