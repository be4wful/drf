from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from .models import User, Product, Cart, Order
from .serializers import UserRegSerializer, UserLoginSerializer, ProductSerializer, CartSerializer, OrderSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegDef(request):
    serializer = UserRegSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'data': {'user_token': Token.objects.create(user=user).key}}, status=HTTP_201_CREATED)
    return Response({'error': {'code': 422, 'message': 'Validation error', 'error': serializer.errors}}, status=HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['POST'])
@permission_classes([AllowAny])
def UserLoginDef(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        except:
            return Response({'error': {'code': 401, 'message': 'Authentication failed'}}, status=401)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'data': {'user_token': token.key}}, status=200)
    return Response({'error': {'code': 422, 'message': 'Validation error', 'error': serializer.errors}}, status=422)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'data': {'message': 'Logout'}})


@api_view(['GET'])
@permission_classes([AllowAny])
def ProductViewDef(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response({'data': serializer.data}, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def ProductAddDef(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return Response({'data': {'id': data['id']}}, status=201)
    return Response({'error': {'code': 422, 'message': 'Validation error', 'error': serializer.errors}}, status=422)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def ProductChangeDeleteDef(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({'error': {'code': 404, 'message': 'Not found'}}, status=404)
    if request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error': {'code': 422, 'message': 'Validation error', 'error': serializer.errors}}, status=422)
    elif request.method == 'DELETE':
        product.delete()
        return Response({'data': {'message': 'Product removed'}}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CartViewDef(request):
    cart = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart, many=True)
    data = serializer.data
    return Response(data, status=200)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def CartAddDeleteView(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': {'code': 404, 'message': 'Not found'}}, status=404)
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return Response({'data': {'message': 'Product added to cart'}}, status=200)
    elif request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        return Response({'data': {'message': 'Product removed from the cart'}}, status=200)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def OrderGetAddView(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        data = serializer.data
        return Response(data, status=200)
    elif request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': {'code': 422, 'message': 'Cart is empty'}}, status=422)
        order = Order.objects.create(user=request.user)
        total = 0
        for product in cart.products.all():
            total += product.price
            order.products.add(product)
        order.order_price = total
        order.save()
        cart.delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)


