import os
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import FileResponse

def upload_document(file, save_dir, filename, allowed_types):
    """
    通用文件上传函数
    :param file: 文件对象 (File类型)
    :param save_dir: 相对项目根目录的存放目录
    :param filename: 保存的文件名(包含扩展名)
    :param allowed_types: 允许的文件类型列表(带点前缀，如['.pdf', '.docx'])
    :return: 包含上传结果的字典
    """
    # 验证文件参数是否为空
    if not file:
        return {
            'success': False,
            'message': '文件不能为空',
            'path': ''
        }

    # 验证文件类型
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in allowed_types:
        return {
            'success': False,
            'message': f'不支持的文件类型，允许类型: {[t.strip(".") for t in allowed_types]}',
            'path': ''
        }

    try:
        # 构建绝对路径（项目根目录+存放目录）
        project_root = settings.BASE_DIR
        absolute_dir = os.path.join(project_root, save_dir)
        absolute_path = os.path.join(absolute_dir, filename)

        # 检查目录是否存在，不存在则创建
        if not os.path.exists(absolute_dir):
            os.makedirs(absolute_dir, exist_ok=True)

        # 保存文件
        with open(absolute_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return {
            'success': True,
            'message': '成功',
            'path': absolute_path
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'文件保存失败: {str(e)}',
            'path': ''
        }







def upload_document(file, save_dir, filename, allowed_types):
    """
    通用文件上传函数
    :param file: 文件对象 (File类型)
    :param save_dir: 相对项目根目录的存放目录
    :param filename: 保存的文件名(包含扩展名)
    :param allowed_types: 允许的文件类型列表(带点前缀，如['.pdf', '.docx'])
    :return: 包含上传结果的字典
    """
    # 验证文件参数是否为空
    if not file:
        return {
            'success': False,
            'message': '文件不能为空',
            'path': ''
        }

    # 验证文件类型
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in allowed_types:
        return {
            'success': False,
            'message': f'不支持的文件类型，允许类型: {[t.strip(".") for t in allowed_types]}',
            'path': ''
        }

    try:
        # 构建绝对路径（项目根目录+存放目录）
        project_root = settings.BASE_DIR
        absolute_dir = os.path.join(project_root, save_dir)
        absolute_path = os.path.join(absolute_dir, filename)

        # 检查目录是否存在，不存在则创建
        if not os.path.exists(absolute_dir):
            os.makedirs(absolute_dir, exist_ok=True)

        # 保存文件
        with open(absolute_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return {
            'success': True,
            'message': '成功',
            'path': absolute_path
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'文件保存失败: {str(e)}',
            'path': ''
        }


def download_document(file_path):
    """
    通用文件下载函数
    :param file_path: 文件绝对路径
    :return: 包含下载结果的字典
    """
    # 验证文件路径参数是否为空
    if not file_path:
        return {
            'success': False,
            'message': '文件路径不能为空',
            'file_response': None
        }

    # 验证文件是否存在
    if not os.path.exists(file_path):
        return {
            'success': False,
            'message': '文件不存在',
            'file_response': None
        }

    # 验证是否为文件且可读
    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
        return {
            'success': False,
            'message': '无法读取文件或路径不是有效的文件',
            'file_response': None
        }

    # 确定MIME类型
    file_ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain'
    }
    content_type = mime_types.get(file_ext, 'application/octet-stream')
    file_name = os.path.basename(file_path)

    # 创建文件响应对象
    try:
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return {
            'success': True,
            'message': '文件准备就绪',
            'file_response': response
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'文件响应创建失败: {str(e)}',
            'file_response': None
        }