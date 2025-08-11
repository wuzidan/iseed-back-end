from rest_framework import status
from rest_framework .response import Response
from rest_framework.decorators import api_view

from api import serializers
from goods.models import books 


@api_view(['GET', 'POST'])
def get_list(request):
    if request.method == 'GET':
        Books = books.objects.all()
        serializer = serializers.booksSerializer(Books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # 对post的数据序列化
        serializer = serializers.booksSerializer(data=request.data)
        # 校验数据
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def index(request):
    print(request.method)
    print(request.path)
    print(request.META)
    print(request.headers)
    print(request.body)
    print(request.POST)
    print(dir(request))
    return Response({'message': 'Hello, World!'})

@api_view(['GET', 'PUT',  'DELETE'])
def books_detail(request,id):
    try:
        book = books.objects.get(id=id)
    except books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.booksSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.booksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def books_add(request):
    if request.method == 'POST':
        serializer = serializers.booksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
