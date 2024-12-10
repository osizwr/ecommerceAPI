from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Order, CartItem
from .serializer import UserSerializer, OrderSerializer, CartItemSerializer

class UsersListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        userID = self.kwargs.get("userID")
        return User.objects.filter(userID=userID)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrdersListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrdersCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrdersRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "orderID"

class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartItemListView(APIView):
    def get(self, request, orderID):
        cart_items = CartItem.objects.filter(orderID=orderID)
        if not cart_items.exists():
            return Response({'error': 'No cart items found for this orderID'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, orderID):
        cart_items = CartItem.objects.filter(orderID=orderID)
        if not cart_items.exists():
            return Response({'error': 'No cart items found for this orderID'}, status=status.HTTP_404_NOT_FOUND)
        
        count = cart_items.delete()[0]  # Returns number of deleted objects
        return Response({'message': f'{count} cart items deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):
    def post(self, request):
        order_id = request.data.get("orderID")
        
        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            order = Order.objects.get(orderID=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if order.status == "PROCESSED":
            return Response({"error": "Order is already processed"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = "PROCESSED"
        order.save()

        return Response(
            {"message": f"Order {order_id} processed successfully", "status": order.status},
            status=status.HTTP_200_OK
        )