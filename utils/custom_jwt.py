from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # 调用父类方法获取基础token
        token = super().get_token(user)
        
        # 添加自定义payload字段
        # 从用户对象获取基本信息
        token['username'] = user.username
        token['user_id'] = user.id
        # 根据用户类型添加特定字段
        # 假设学生模型有s_num字段，教师模型有t_num字段
        if hasattr(user, 's_num'):
            token['user_type'] = 'student'
            token['num'] = user.s_num
        elif hasattr(user, 't_num'):
            token['user_type'] = 'teacher'
            token['num'] = user.t_num


        # # 添加额外自定义字段
        # token['is_active'] = user.is_active
        
        return token