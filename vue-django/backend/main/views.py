import re

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Role,User,Customer,Port,Cargo,OrderCargo,Order,Task,Track,FaultReport,Permission,Role_Permission
import hashlib
import json
from django.views.decorators.csrf import csrf_exempt

def check_login(username,password):
    if '@' in username:
        try:
            user=User.objects.get(email=username)
        except User.DoesNotExist:
            return False
        hash_password=hashlib.sha256(password.encode()).hexdigest()
        if  user.password==hash_password:
            return True
    else:   
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return False
        hash_password=hashlib.sha256(password.encode()).hexdigest()
        if  user.password==hash_password:
            return True
    return False

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     remember_me = request.data.get('remember')
#     print(request.method)
#     print(request.body)
#     if not username or not password:
#         return Response({"success": False, "msg": "请输入用户名和密码"})

#     if not check_login(username, password):
#         return Response({"success": False, "msg": "账号或密码错误"})

#     # 查用户
#     if '@' in username:
#         user = User.objects.filter(email=username).first()
#     else:
#         user = User.objects.filter(username=username).first()

#     if not user:
#         return Response({"success": False, "msg": "用户不存在"})

#     if user.status == "已禁用":
#         return Response({"success": False, "msg": "该用户已被禁用"})

#     # session（可留）
#     request.session['user_info'] = {
#         'id': user.user_id,
#         'name': user.username,
#         'role': user.role.role_name if user.role else '未知角色',
#         'avatar': user.photo,
#     }

#     if remember_me:
#         request.session.set_expiry(60 * 60 * 24 * 7)
#     else:
#         request.session.set_expiry(0)

#     # 更新状态
#     user.last_visit = timezone.now()
#     user.login_status = True
#     user.save(update_fields=['last_visit', 'login_status'])

#     # 返回给前端（重点）
#     return Response({
#         "success": True,
#         "msg": "登录成功",
#         "user": {
#             "id": user.user_id,
#             "name": user.username,
#             "role": user.role.role_name if user.role else '未知角色',
#         }
#     })

@csrf_exempt
def login(request):
    print("method:", request.method)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': '仅支持 POST'})

    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print("JSON错误:", e)
        return JsonResponse({'success': False, 'msg': 'JSON解析失败'})

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'success': False, 'msg': '参数缺失'})

    try:
        if check_login(username, password):

            if '@' in username:
                user = User.objects.filter(email=username).first()
            else:
                user = User.objects.filter(username=username).first()

            if not user:
                return JsonResponse({'success': False, 'msg': '用户不存在'})

            role_name = user.role.role_name if user.role else '未知角色'
            request.session['user_info'] = {
                'id': user.user_id,
                'name': user.username,
                'role': user.role.role_name if user.role else '未知',
                'avatar': user.photo,
            }
            request.session.modified = True
            request.session.save()
            print("session key:", request.session.session_key)
            return JsonResponse({
                'success': True,
                'user': {
                    'name': user.username,
                    'role': role_name,
                    'avatar': user.photo if user.photo else ''
                }
            })

        else:
            return JsonResponse({'success': False, 'msg': '账号或密码错误'})

    except Exception as e:
        print("后端炸了:", e)
        return JsonResponse({'success': False, 'msg': '服务器错误'})


def change_password(username,password,password2):
    error=[]
    if password!=password2:
        error.append("两次输入的密码不一致")
        return error
    
    if len(password)<6:
        error.append("密码长度至少6位")
        return error
    if not re.search(r'[a-z]', password):
        error.append("密码必须包含小写字母")
        return error
    if not re.search(r'[A-Z]', password):
        error.append("密码必须包含大写字母")
        return error
    if not re.search(r'\d', password):
        error.append("密码必须包含数字")
        return error
    
    if '@' not in username:
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            error.append("用户不存在")
            return error
    else:
        try:
            user=User.objects.get(email=username)
        except User.DoesNotExist:
            error.append("用户不存在")
            return error
        
    if user.status!="已启用":
        error.append("用户账户已被禁用，无法修改密码")
        return error
    
    try:
        hash_passowrd=hashlib.sha256(password.encode()).hexdigest()
        user.password=hash_passowrd
        user.save()
    except Exception as e:
        error.append(f"密码修改失败: {str(e)}")
        return error
    return True

@csrf_exempt
def retrieve_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')

        msg = change_password(username, password, password2)

        if msg == True:
            return JsonResponse({'success': True, 'msg': '修改成功'})
        else:
            return JsonResponse({'success': False, 'msg': '\n'.join(msg)})

    return JsonResponse({'success': False, 'msg': '仅支持 POST'})


from django.db.models import Sum, Count
from django.db import connection

def report_dashboard(request):
    if request.method != 'GET':
        return JsonResponse({"success": False, "msg": "仅支持 GET"})

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_cargo_types = Cargo.objects.count()

    cargo_agg = Cargo.objects.aggregate(total=Sum('inventory'))
    cargo_total_amount = cargo_agg.get('total') or 0

    order_status_count = list(
        Order.objects.values('order_status')
        .annotate(count=Count('order_status'))
        .order_by('order_status')
    )

    monthly_orders = []
    cargo_top_5 = []

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT month, count 
            FROM v_report_monthly_orders 
            ORDER BY month
        """)
        rows = cursor.fetchall()
        for row in rows:
            monthly_orders.append({
                'month': row[0],
                'count': row[1]
            })

        cursor.execute("""
            SELECT cargo_name, total_inventory 
            FROM v_report_cargo_stats 
            ORDER BY total_inventory DESC 
            LIMIT 5
        """)
        rows = cursor.fetchall()
        for row in rows:
            cargo_top_5.append({
                'cargo_name': row[0],
                'total': row[1]
            })

    return JsonResponse({
        "success": True,
        "data": {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_cargo_types": total_cargo_types,
            "cargo_total_amount": cargo_total_amount,
            "order_status_count": order_status_count,
            "monthly_orders": monthly_orders,
            "cargo_top_5": cargo_top_5,
        }
    })

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_GET

@require_GET
def user_management(request):
    # 当前登录用户
    user_info = request.session.get('user_info', {})
    current_user_id = user_info.get('id')

    # 参数
    keyword = request.GET.get('keyword', '').strip()
    page_number = request.GET.get('page', 1)

    # 查询用户 + 角色（避免N+1）
    users_qs = User.objects.select_related('role').all().order_by('user_id')

    if keyword:
        users_qs = users_qs.filter(
            Q(username__icontains=keyword) |
            Q(role__role_name__icontains=keyword) |
            Q(status__icontains=keyword)
        )

    # 分页
    paginator = Paginator(users_qs, 10)
    page_obj = paginator.get_page(page_number)

    # ===== 批量查权限（优化重点，避免循环查）=====
    role_ids = [u.role.role_id for u in page_obj if u.role]

    role_perm_map = {}
    if role_ids:
        rp_list = Role_Permission.objects.filter(role_id__in=role_ids)
        perm_map = {}

        for rp in rp_list:
            perm_map.setdefault(rp.role_id, []).append(rp.permission_id)

        perms = Permission.objects.filter(
            perm_id__in=[pid for pids in perm_map.values() for pid in pids]
        )

        perm_name_map = {p.perm_id: p.perm_name for p in perms}

        for role_id, pids in perm_map.items():
            role_perm_map[role_id] = [perm_name_map.get(pid) for pid in pids]

    # ===== 组装数据 =====
    user_list = []
    for u in page_obj:
        user_list.append({
            "id": u.user_id,
            "username": u.username,
            "role": u.role.role_name if u.role else None,
            "permissions": role_perm_map.get(u.role.role_id, []) if u.role else [],
            "phone": u.phone,
            "email": u.email,
            "status": u.status,
            "last_visit": u.last_visit.strftime("%Y-%m-%d %H:%M") if u.last_visit else None,
            "is_self": u.user_id == current_user_id
        })

    # ===== 返回JSON =====
    return JsonResponse({
        "success": True,
        "data": {
            "users": user_list,
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_count": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
    })


@csrf_exempt
def toggle_user_status(request, user_id):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            action = data.get("action")
            user = User.objects.get(user_id=user_id)

            if action == "启用":
                user.status = "已启用"
            else:
                user.status = "已禁用"
            user.save()

            return JsonResponse({"success": True, "message": f"用户状态已更新为 {user.status}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "非法请求方式"})


# 获取个人信息
def get_profile(request):
    # print(request.session.items())
    # print(request.COOKIES)
    user_id = request.session.get('user_id')
    # print(user_id)
    if not user_id:
        return JsonResponse({"success": False, "message": "未登录"})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "用户不存在"})

    return JsonResponse({
        "success": True,
        "data": {
            "id": user.user_id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "role": user.role.role_name if user.role else '',
            "avatar": user.photo
        }
    })

import json, os, uuid
from django.conf import settings
# 更新个人信息（支持头像）
@csrf_exempt
def administrator_update_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "非法请求"})

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({"success": False, "message": "未登录"})

    

    try:
        user = User.objects.get(user_id=user_id)

        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        avatar_file = request.FILES.get("avatar")

        user.username = username
        user.phone = phone
        user.email = email

        if avatar_file:
            ext = os.path.splitext(avatar_file.name)[1]
            filename = f"{uuid.uuid4().hex}{ext}"

            save_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(save_dir, exist_ok=True)

            file_path = os.path.join(save_dir, filename)

            with open(file_path, 'wb+') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)

            user.photo = f'/media/avatars/{filename}'

        user.save()

        # 更新 session
        request.session['user_info'] = {
            'id': user.user_id,
            'name': user.username,
            'role': user.role.role_name if user.role else '',
            'avatar': user.photo,
        }

        return JsonResponse({"success": True, "message": "更新成功"})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

from django.db.models.functions import TruncMonth
def operator_report(request):
    # ===== KPI =====
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_cargo_types = Cargo.objects.count()
    total_tasks = Task.objects.count()

    # ===== 订单状态 =====
    order_status = list(
        Order.objects
        .values('order_status')
        .annotate(count=Count('order_id'))
    )

    # ===== 月度订单（已修复）=====
    monthly_qs = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('order_id'))
        .order_by('month')
    )

    monthly_orders = [
        {
            "month": item["month"].strftime("%Y-%m") if item["month"] else "",
            "count": item["count"]
        }
        for item in monthly_qs
    ]

    # ===== 货物 TOP5 =====
    cargo_top = list(
        Cargo.objects
        .values('cargo_name')
        .annotate(total=Count('cargo_id'))
        .order_by('-total')[:5]
    )

    return JsonResponse({
        "kpi": {
            "users": total_users,
            "orders": total_orders,
            "cargo": total_cargo_types,
            "tasks": total_tasks,
        },
        "order_status": order_status,
        "monthly_orders": monthly_orders,
        "cargo_top": cargo_top
    })


def operator_user_info_api(request):
    user_info = request.session.get('user_info') or {}
    print(user_info)
    return JsonResponse({
        "name": user_info.get("name"),
        "avatar": user_info.get("avatar"),
        "role": user_info.get("role"),
    })