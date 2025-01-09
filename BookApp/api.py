from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .models import BookModel
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'
    def validate(self,data):
        price = data['price']
        if price < 0:
            raise serializers.ValidationError('price must be positive')
        return data

# @api_view(['GET'])
# def BookListApi(request):
#     # fetch book from database
#     books = BookModel.objects.all()
#     serializers = BookSerializer(books,many = True)

#     # send response
#     return Response(serializers.data)

# @api_view(['POST'])
# def BookCreateApi(request):
#     #request data
#     data = request.data
#     serializers = BookSerializer(data = data)
#     if serializers.is_valid():
#         serializers.save()   
#         return Response({
#         'message' : 'book create'
#         })
#     return Response(serializers.errors)

# @api_view(['PUT'])
# def BookUpdateApi(request,id):
#     data = request.data
#     book = BookModel.objects.get(id = id)
#     serializers = BookSerializer(instance = book,data = data)
#     if serializers.is_valid():
#         serializers.save()
#         return Response({
#         'message' : 'book updated'
#         })
#     return Response(serializers.errors)

# @api_view(['DELETE'])
# def BookDeleteApi(request,id):
#     book = BookModel.objects.get(id = id)
#     book.delete()
#     return Response({
#         'message' : 'book deleted'
#     })

class CustomPagination(CursorPagination):
    page_size = 2
    ordering = 'price'


class Bookviewset(ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def list(self,request):
        user = request.user
        books = BookModel.objects.filter(author = user)
        page = self.paginate_queryset(books)
        serializers = self.get_serializer(page,many = True)
        return self.get_paginated_response(serializers.data)
    
    def create(self,request):
        # name,price
        data = request.data
        # author
        user = request.user
        serializers = self.get_serializer(data = data)
        if serializers.is_valid():
            serializers.save(author = user)
            return Response({
                'message' : 'book created'
            })
        return Response(serializers.errors)
    
    def update(self,request,pk):
        book = BookModel.objects.get(id = pk)
        # check if user is author of book
        if book.author == request.user:
            data = request.data
            serializers = self.get_serializer(instance = book,data = data)
            if serializers.is_valid():
                serializers.save()
                return Response({
                    'message' : 'book updated'
                })
            return Response(serializers.errors)
        else:
            return Response({
                'message' : 'you are not author of this book'
            })
        
    def destroy(self,request,pk):
        book = BookModel.objects.get(id = pk)
        # check if user is author of book
        if book.author == request.user:
            book.delete()
            return Response({
                'message' : 'book deleted'
            })
        else:
            return Response({
                'message' : 'you are not author of this book'
            })
        
