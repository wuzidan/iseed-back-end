#序列化器文件：在数据库模型与json格式之间转换
#作用：
#- 序列化 ：把数据库中的书籍数据转换成 JSON 格式，这样前端（如网页、手机APP）才能理解和显示
#- 反序列化 ：把前端发送过来的 JSON 数据转换成数据库能存储的格式
#- 数据验证 ：自动检查输入数据是否符合要求（比如必填字段是否为空、数据类型是否正确等）
from rest_framework import serializers
from goods import models
from goods.models import books
#处理数据与复杂数据类型转换工具

class booksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.books
        fields = '__all__'
