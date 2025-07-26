from rest_framework import serializers

from goods import models
from goods.models import books
#处理数据与复杂数据类型转换工具

class booksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.books
        fields = '__all__'