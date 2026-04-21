import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

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

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Customer

def customer_list_api(request):
    page_number = request.GET.get('page', 1)
    keyword = request.GET.get('keyword', '').strip()

    customers = Customer.objects.all().order_by('customer_id')

    if keyword:
        customers = customers.filter(
            Q(customer_name__icontains=keyword) |
            Q(customer_phone__icontains=keyword) |
            Q(customer_email__icontains=keyword)
        )

    paginator = Paginator(customers, 10)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "customer_id": c.customer_id,
            "customer_name": c.customer_name,
            "customer_email": c.customer_email,
            "customer_phone": c.customer_phone,
            "customer_address": c.customer_address,
        }
        for c in page_obj
    ]

    return JsonResponse({
        "success": True,
        "data": {
            "customers": data,
            "pagination": {
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "total_count": paginator.count,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
    })

@api_view(['POST'])
def create_customer_api(request):
    data = request.data

    name = data.get('customer_name', '').strip()
    phone = data.get('customer_phone', '').strip()
    email = data.get('customer_email', '').strip()
    address = data.get('customer_address', '').strip()

    if not name or not phone or not address:
        return Response({'msg': '必填项不能为空'}, status=400)

    if len(phone) != 11 or not phone.isdigit():
        return Response({'msg': '手机号不合法'}, status=400)

    if Customer.objects.filter(customer_phone=phone).exists():
        return Response({'msg': '手机号已存在'}, status=400)

    Customer.objects.create(
        customer_name=name,
        customer_phone=phone,
        customer_email=email,
        customer_address=address
    )

    return Response({'msg': 'success'})

@csrf_exempt
def edit_customer(request, customer_id):
    customer = Customer.objects.get(customer_id=customer_id)

    data = json.loads(request.body)

    customer.customer_name = data["customer_name"]
    customer.customer_phone = data["customer_phone"]
    customer.customer_email = data.get("customer_email", "")
    customer.customer_address = data["customer_address"]
    customer.save()

    return JsonResponse({"code": 0, "msg": "updated"})


@csrf_exempt
def delete_customer(request, customer_id):
    if request.method == "DELETE":
        customer = Customer.objects.get(customer_id=customer_id)
        customer.delete()
        return JsonResponse({"msg": "ok"})

def customer_detail(request, customer_id):
    customer = Customer.objects.get(customer_id=customer_id)

    return JsonResponse({
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "customer_phone": customer.customer_phone,
        "customer_email": customer.customer_email,
        "customer_address": customer.customer_address,
    })

def port_list_api(request):
    page = request.GET.get("page", 1)
    keyword = request.GET.get("keyword", "").strip()

    qs = Port.objects.all().order_by("port_id")

    if keyword:
        qs = qs.filter(
            Q(port_code__icontains=keyword) |
            Q(port_name__icontains=keyword) |
            Q(port_name_en__icontains=keyword) |
            Q(country__icontains=keyword) |
            Q(city__icontains=keyword)
        )

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for p in page_obj:
        data.append({
            "port_id": p.port_id,
            "port_code": p.port_code,
            "port_name": p.port_name,
            "port_name_en": p.port_name_en,
            "country": p.country,
            "city": p.city,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "contact_person": p.contact_person,
            "contact_phone": p.contact_phone,
            "status": p.status,
        })

    return JsonResponse({
    # ===== 旧结构（完全保留）=====
    "list": data,
    "page": page_obj.number,
    "total_pages": paginator.num_pages,
    "total": paginator.count,
    "has_next": page_obj.has_next(),
    "has_previous": page_obj.has_previous(),

    # ===== 新结构（新增，不影响旧代码）=====
    "success": True,
    "data": {
        "list": data,
        "pagination": {
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
            "total": paginator.count,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        }
    }
})

import json
from django.http import JsonResponse
from .models import Port
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_port_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Port.objects.create(
            port_code=data.get("port_code"),
            port_name=data.get("port_name"),
            port_name_en=data.get("port_name_en"),
            city=data.get("city"),
            country=data.get("country"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            contact_person=data.get("contact_person"),
            contact_phone=data.get("contact_phone"),
            status=data.get("status"),
        )

        return JsonResponse({"msg": "ok"})
    

from django.forms.models import model_to_dict
@csrf_exempt
def port_detail(request, port_id):
    port = Port.objects.get(port_id=port_id)

    if request.method == "GET":
        return JsonResponse(model_to_dict(port))

    elif request.method == "PUT":
        data = json.loads(request.body)

        for k, v in data.items():
            setattr(port, k, v)

        port.save()
        return JsonResponse({"msg": "updated"})

    elif request.method == "DELETE":
        port.delete()
        return JsonResponse({"msg": "deleted"})
    
@csrf_exempt
def delete_port(request, port_id):
    print(111)
    if request.method == "DELETE":
        port = Port.objects.get(port_id=port_id)
        port.delete()
        return JsonResponse({"msg": "ok"})
    
def cargo_list(request):
    keyword = request.GET.get("keyword", "")
    page = int(request.GET.get("page", 1))

    qs = Cargo.objects.all()

    if keyword:
        qs = qs.filter(cargo_name__icontains=keyword)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for c in page_obj:
        data.append({
            "cargo_id": c.cargo_id,
            "cargo_name": c.cargo_name,
            "cargo_type": c.cargo_type,
            "cargo_weight": c.cargo_weight,
            "cargo_volume": c.cargo_volume,
            "cargo_amount": c.cargo_amount,
            "inventory": c.inventory
        })

    return JsonResponse({
        # ===== 老结构（不动）=====
        "list": data,
        "page": page,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),

        # ===== 新结构（新增）=====
        "success": True,
        "data": {
            "list": data,
            "pagination": {
                "page": page,
                "total_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }
    })

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_cargo_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Cargo.objects.create(
            cargo_name=data.get("cargo_name"),
            cargo_type=data.get("cargo_type"),
            cargo_weight=data.get("cargo_weight"),
            cargo_volume=data.get("cargo_volume"),
            inventory=data.get("inventory"),
            cargo_amount=data.get("cargo_amount"),
        )

        return JsonResponse({"msg": "ok"})

from django.http import JsonResponse
from django.forms.models import model_to_dict
@csrf_exempt
def edit_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, cargo_id=cargo_id)

    if request.method == 'GET':
        return JsonResponse(model_to_dict(cargo))

    if request.method == 'PUT':
        import json
        data = json.loads(request.body)

        try:
            cargo_name = data.get('cargo_name', '').strip()
            cargo_type = data.get('cargo_type', '').strip()
            cargo_weight = float(data.get('cargo_weight'))
            cargo_volume = float(data.get('cargo_volume'))
            inventory = int(data.get('inventory'))
            cargo_amount = float(data.get('cargo_amount'))

            if cargo_weight < 0 or cargo_volume < 0 or inventory < 0 or cargo_amount < 0:
                return JsonResponse({'error': '不能为负数'}, status=400)

            cargo.cargo_name = cargo_name
            cargo.cargo_type = cargo_type
            cargo.cargo_weight = cargo_weight
            cargo.cargo_volume = cargo_volume
            cargo.inventory = inventory
            cargo.cargo_amount = cargo_amount
            cargo.save()

            return JsonResponse({'msg': 'success'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_cargo(request, id):
    if request.method == "DELETE":
        Cargo.objects.filter(cargo_id=id).delete()
        return JsonResponse({"msg": "ok"})
    
from django.http import JsonResponse
from django.core.paginator import Paginator

from django.db.models import Case, When, Value, IntegerField, Q

def get_orders_sorted_from_view(keyword=''):
    from .models import Order

    qs = Order.objects.all()

    # 🔥 状态排序权重
    qs = qs.annotate(
        status_order=Case(
            When(order_status='草稿', then=Value(0)),
            When(order_status='待指派', then=Value(1)),
            When(order_status='已指派', then=Value(2)),
            When(order_status='运输中', then=Value(3)),
            When(order_status='已完成', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    ).order_by('status_order', '-created_at')  # ⭐先按状态，再按时间

    # 🔍 搜索
    if keyword:
        qs = qs.filter(
            Q(customer__customer_name__icontains=keyword) |
            Q(origin_port__icontains=keyword) |
            Q(destination_port__icontains=keyword) |
            Q(order_status__icontains=keyword)
        )

    # 转 JSON
    data = []
    for o in qs:
        data.append({
            'order_id': o.order_id,
            'customer_name': o.customer.customer_name if o.customer else '',
            'origin_port_name': o.origin_port,
            'destination_port_name': o.destination_port,
            'order_status': o.order_status,
            'total_amount': float(o.total_amount),
            'created_at': o.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': o.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return data
def orders_list(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return JsonResponse({'success': False, 'message': '未登录'}, status=401)

    page_number = request.GET.get('page', 1)
    keyword = request.GET.get('keyword', '').strip()

    orders_data = get_orders_sorted_from_view(keyword)

    paginator = Paginator(orders_data, 10)
    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        'success': True,
        'data': {
            'list': list(page_obj.object_list),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

@csrf_exempt
@transaction.atomic
def create_order_api(request):

    if request.method != "POST":
        return JsonResponse({"error": "仅支持 POST"}, status=405)

    try:
        data = json.loads(request.body)

        # ===== 用户 =====
        user_info = request.session.get('user_info')
        if not user_info:
            return JsonResponse({"error": "未登录"}, status=401)

        created_by = User.objects.get(username=user_info['name'])

        # ===== 参数提取（必须在校验前）=====
        origin_port_id = data.get('origin_port')
        destination_port_id = data.get('destination_port')
        customer_id = data.get('customer')
        cargo_list = data.get("cargo_list", [])
        is_draft = data.get('is_draft', False)

        # ===== 参数校验 =====
        if not customer_id:
            return JsonResponse({"error": "请选择客户"}, status=400)

        if not origin_port_id or not destination_port_id:
            return JsonResponse({"error": "请选择港口"}, status=400)

        if origin_port_id == destination_port_id:
            return JsonResponse({"error": "始发港和目的港不能相同"}, status=400)

        if not cargo_list:
            return JsonResponse({"error": "请至少添加一个货物"}, status=400)

        # ===== 查港口 =====
        origin_port = Port.objects.filter(port_id=origin_port_id).first()
        destination_port = Port.objects.filter(port_id=destination_port_id).first()

        origin_port_name = origin_port.port_name if origin_port else None
        destination_port_name = destination_port.port_name if destination_port else None

        # ===== 客户 =====
        customer = Customer.objects.filter(customer_id=customer_id).first()

        # ===== 状态 =====
        order_status = "草稿" if is_draft else "待指派"

        # ===== 库存检查 =====
        for item in cargo_list:
            cargo = Cargo.objects.select_for_update().get(
                cargo_id=item["cargo_id"]
            )
            if cargo.inventory < int(item["quantity"]):
                return JsonResponse({
                    "error": f"货物【{cargo.cargo_name}】库存不足（剩余 {cargo.inventory}）"
                }, status=400)

        # ===== 创建订单 =====
        order = Order.objects.create(
            created_by=created_by,
            customer=customer,
            origin_port=origin_port_name,
            destination_port=destination_port_name,
            order_status=order_status,
            total_amount=0
        )

        total_amount = 0

        # ===== 写入订单货物 + 扣库存 =====
        for item in cargo_list:
            cargo = Cargo.objects.select_for_update().get(
                cargo_id=item["cargo_id"]
            )
            quantity = int(item["quantity"])

            cargo.inventory -= quantity
            cargo.save()

            OrderCargo.objects.create(
                cargo=cargo,
                order=order,
                quantity=quantity
            )

            total_amount += cargo.cargo_amount * quantity

        order.total_amount = total_amount
        order.save()

        return JsonResponse({
            "message": "订单创建成功",
            "order_id": order.order_id
        })

    except Exception as e:
        print("❌ 创建订单失败:", e)
        return JsonResponse({"error": str(e)}, status=500)
def get_port_id(name):
    """根据港口名获取ID（安全版）"""
    if not name:
        return None
    try:
        return Port.objects.get(port_name=name).port_id
    except Port.DoesNotExist:
        return None

def get_order_detail(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    if not order:
        return JsonResponse({"error": "订单不存在"}, status=404)

    # ===== 货物 =====
    cargos = OrderCargo.objects.filter(order=order)
    cargo_list = []
    for oc in cargos:
        cargo_list.append({
            "cargo_id": oc.cargo.cargo_id,
            "cargo_name": oc.cargo.cargo_name,
            "quantity": oc.quantity
        })

    # ===== 返回 =====
    return JsonResponse({
        "order_id": order.order_id,

        # ✅ 客户（关键）
        "customer": order.customer.customer_id if order.customer else None,
        "customer_name": order.customer.customer_name if order.customer else None,

        # ✅ 港口（兼容你现在的字符串设计）
        "origin_port": get_port_id(order.origin_port),
        "origin_port_name": order.origin_port,

        "destination_port": get_port_id(order.destination_port),
        "destination_port_name": order.destination_port,

        # ✅ 货物
        "cargo_list": cargo_list
    })

@csrf_exempt
@transaction.atomic
def update_order_api(request, order_id):
    if request.method != "POST":
        return JsonResponse({"error": "仅支持 POST"}, status=405)

    try:
        data = json.loads(request.body)

        order = Order.objects.select_for_update().filter(order_id=order_id).first()
        if not order:
            return JsonResponse({"error": "订单不存在"}, status=404)

        if order.order_status not in ["草稿", "待指派"]:
            return JsonResponse({"error": "该订单不可修改"}, status=400)

        customer_id = data.get("customer")
        origin_port_id = data.get("origin_port")
        destination_port_id = data.get("destination_port")
        cargo_list = data.get("cargo_list", [])
        is_draft = data.get("is_draft", False)

        if not customer_id:
            return JsonResponse({"error": "请选择客户"}, status=400)

        if not origin_port_id or not destination_port_id:
            return JsonResponse({"error": "请选择港口"}, status=400)

        if origin_port_id == destination_port_id:
            return JsonResponse({"error": "始发港和目的港不能相同"}, status=400)

        if not cargo_list:
            return JsonResponse({"error": "请添加货物"}, status=400)

        customer = Customer.objects.filter(customer_id=customer_id).first()
        origin_port = Port.objects.filter(port_id=origin_port_id).first()
        destination_port = Port.objects.filter(port_id=destination_port_id).first()

        # ===== 还原库存 =====
        old_items = OrderCargo.objects.filter(order=order)
        for oc in old_items:
            cargo = Cargo.objects.select_for_update().get(cargo_id=oc.cargo.cargo_id)
            cargo.inventory += oc.quantity
            cargo.save()

        old_items.delete()

        # ===== 检查库存 =====
        for item in cargo_list:
            cargo = Cargo.objects.select_for_update().get(cargo_id=item["cargo_id"])
            if cargo.inventory < int(item["quantity"]):
                return JsonResponse({
                    "error": f"{cargo.cargo_name} 库存不足"
                }, status=400)

        # ===== 写入新数据 =====
        total_amount = 0

        for item in cargo_list:
            cargo = Cargo.objects.select_for_update().get(cargo_id=item["cargo_id"])
            qty = int(item["quantity"])

            cargo.inventory -= qty
            cargo.save()

            OrderCargo.objects.create(
                order=order,
                cargo=cargo,
                quantity=qty
            )

            total_amount += cargo.cargo_amount * qty

        order.customer = customer
        order.origin_port = origin_port.port_name
        order.destination_port = destination_port.port_name
        order.order_status = "草稿" if is_draft else "待指派"
        order.total_amount = total_amount
        order.save()

        return JsonResponse({"message": "修改成功"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@transaction.atomic
def delete_order_api(request, order_id):

    if request.method != "DELETE":
        return JsonResponse({"error": "仅支持 DELETE"}, status=405)

    try:
        # ===== 登录校验 =====
        user_info = request.session.get('user_info')
        if not user_info:
            return JsonResponse({"error": "未登录"}, status=401)

        # ===== 查订单 =====
        order = get_object_or_404(Order, order_id=order_id)

        # ❗可选：限制已完成订单不能删除
        if order.order_status == "已完成":
            return JsonResponse({"error": "已完成订单不可删除"}, status=400)

        # ===== 回滚库存（加锁）=====
        order_cargos = OrderCargo.objects.select_for_update().filter(order=order)

        for oc in order_cargos:
            cargo = Cargo.objects.select_for_update().get(
                cargo_id=oc.cargo.cargo_id
            )
            cargo.inventory += oc.quantity
            cargo.save()

        # ===== 删除关联表 =====
        order_cargos.delete()

        # ===== 删除订单 =====
        order.delete()

        return JsonResponse({
            "message": "订单删除成功"
        })

    except Exception as e:
        print("❌ 删除订单失败：", e)
        return JsonResponse({
            "error": str(e)
        }, status=500)


    
from django.http import JsonResponse

def operator_get_profile(request):
    user_info = request.session.get('user_info')
    user_id=user_info['id']
    print(user_id)
    if not user_id:
        return JsonResponse({
            "success": False,
            "message": "未登录"
        })

    try:
        user = User.objects.select_related('role').get(user_id=user_id)

        return JsonResponse({
            "success": True,
            "data": {
                "id": user.user_id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "role": user.role.role_name if user.role else "操作员",
                "avatar": user.photo or ""
            }
        })

    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "用户不存在"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })
import os, uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def operator_update_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "非法请求"})
    user_info = request.session.get('user_info')
    user_id=user_info['id']
    if not user_id:
        return JsonResponse({"success": False, "message": "未登录"})

    try:
        user = User.objects.get(user_id=user_id)
        user.user_id=user_id
        # ===== 获取表单数据 =====
        username = request.POST.get("username", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        avatar_file = request.FILES.get("avatar")

        # ===== 基础校验 =====
        if not username or not phone or not email:
            return JsonResponse({
                "success": False,
                "message": "用户名、电话、邮箱不能为空"
            })

        # ===== 更新字段 =====
        user.username = username
        user.phone = phone
        user.email = email

        # ===== 头像处理 =====
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

        # ===== 更新 session =====
        request.session['user_info'] = {
            'id': user.user_id,
            'name': user.username,
            'role': user.role.role_name if user.role else '操作员',
            'avatar': user.photo,
        }

        return JsonResponse({
            "success": True,
            "message": "更新成功",
            "data": {
                "id": user.user_id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "avatar": user.photo,
                "role": user.role.role_name if user.role else '操作员'
            }
        })

    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "用户不存在"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
import json

@api_view(['GET'])
def appointer_dashboard(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return Response({'error': '未登录'}, status=401)

    current_user_id = user_info.get('id')

    pending_orders_count = Order.objects.filter(order_status='待指派').count()

    my_active_tasks_count = Task.objects.filter(
        assigned_by_id=current_user_id,
        task_status='运输中'
    ).count()

    my_pending_faults = FaultReport.objects.filter(
        task_id__assigned_by_id=current_user_id,
        status='待处理'
    ).count()

    my_completed_tasks = Task.objects.filter(
        assigned_by_id=current_user_id,
        task_status='已完成'
    ).count()

    task_status_data = (
        Task.objects.filter(assigned_by_id=current_user_id)
        .values('task_status')
        .annotate(count=Count('task_id'))
    )

    pie_data = [
        {'name': item['task_status'], 'value': item['count']}
        for item in task_status_data
    ]

    recent_tasks = list(
        Task.objects.filter(assigned_by_id=current_user_id)
        .select_related('assigned_to')
        .order_by('-assigned_time')[:5]
        .values(
            'task_id',
            'origin_port',
            'destination_port',
            'task_status',
            'assigned_time',
            'assigned_to__username'
        )
    )

    return Response({
        'user_info': user_info,
        'pending_orders_count': pending_orders_count,
        'my_active_tasks_count': my_active_tasks_count,
        'my_pending_faults': my_pending_faults,
        'my_completed_tasks': my_completed_tasks,
        'pie_data': pie_data,
        'recent_tasks': recent_tasks
    })

from django.http import JsonResponse

def appointer_get_profile(request):
    user_info = request.session.get('user_info')

    if not user_info:
        return JsonResponse({
            "success": False,
            "message": "未登录"
        })

    user_id = user_info.get('id')

    if not user_id:
        return JsonResponse({
            "success": False,
            "message": "用户信息异常"
        })

    try:
        user = User.objects.select_related('role').get(user_id=user_id)

        return JsonResponse({
            "success": True,
            "data": {
                "id": user.user_id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "role": user.role.role_name if user.role else "指派员",
                "avatar": user.photo or ""
            }
        })

    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "用户不存在"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })
    
    import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def appointer_update_profile(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "非法请求"
        })

    user_info = request.session.get('user_info')

    if not user_info:
        return JsonResponse({
            "success": False,
            "message": "未登录"
        })

    user_id = user_info.get('id')

    if not user_id:
        return JsonResponse({
            "success": False,
            "message": "用户信息异常"
        })

    try:
        user = User.objects.get(user_id=user_id)

        # ===== 获取数据 =====
        username = request.POST.get("username", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        avatar_file = request.FILES.get("avatar")

        # ===== 校验 =====
        if not username or not phone or not email:
            return JsonResponse({
                "success": False,
                "message": "用户名、电话、邮箱不能为空"
            })

        # ===== 更新基本信息 =====
        user.username = username
        user.phone = phone
        user.email = email

        # ===== 头像处理（优化版）=====
        if avatar_file:
            ext = os.path.splitext(avatar_file.name)[1]
            filename = f"{uuid.uuid4().hex}{ext}"

            save_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            os.makedirs(save_dir, exist_ok=True)

            file_path = os.path.join(save_dir, filename)

            with open(file_path, 'wb+') as f:
                for chunk in avatar_file.chunks():
                    f.write(chunk)

            # 删除旧头像（避免垃圾文件）
            if user.photo:
                old_path = os.path.join(settings.BASE_DIR, user.photo.lstrip('/'))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except:
                        pass

            user.photo = f'/media/avatars/{filename}'

        user.save()

        # ===== 更新 session（关键）=====
        request.session['user_info'] = {
            'id': user.user_id,
            'name': user.username,
            'role': user.role.role_name if user.role else '指派员',
            'avatar': user.photo,
        }

        return JsonResponse({
            "success": True,
            "message": "更新成功",
            "data": {
                "id": user.user_id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "avatar": user.photo,
                "role": user.role.role_name if user.role else '指派员'
            }
        })

    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "用户不存在"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })


from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

def api_assign_orders(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return JsonResponse({"success": False, "message": "未登录"})

    keyword = request.GET.get('keyword', '').strip()
    page = int(request.GET.get('page', 1))

    orders = Order.objects.exclude(order_status='草稿')

    if keyword:
        orders = orders.filter(
            Q(origin_port__icontains=keyword) |
            Q(destination_port__icontains=keyword) |
            Q(customer__customer_name__icontains=keyword) |
            Q(order_status__icontains=keyword)
        )

    orders = orders.select_related('customer').order_by('order_id')

    # 状态排序（关键）
    status_order = {
        '待指派': 0,
        '运输中': 1,
        '已完成': 2,
    }

    orders = sorted(
        orders,
        key=lambda r: status_order.get(r.order_status, 3)
    )

    paginator = Paginator(orders, 10)
    page_obj = paginator.get_page(page)

    data = []
    for o in page_obj:
        data.append({
            "order_id": o.order_id,
            "customer_name": o.customer.customer_name,
            "origin_port": o.origin_port,
            "destination_port": o.destination_port,
            "order_status": o.order_status,
            "total_amount": float(o.total_amount),
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": o.updated_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({
        "success": True,
        "data": data,
        "pagination": {
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
        }
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order, OrderCargo

def appointer_get_order_detail(request, order_id):
    user_info = request.session.get('user_info')

    if not user_info:
        return JsonResponse({"success": False, "message": "未登录"})

    try:
        order = get_object_or_404(
            Order.objects.select_related('customer', 'task'),
            order_id=order_id
        )

        cargos = OrderCargo.objects.select_related('cargo').filter(order=order)

        cargo_list = []
        for c in cargos:
            cargo_list.append({
                "cargo_name": c.cargo.cargo_name,
                "cargo_type": c.cargo.cargo_type,
                "cargo_weight": c.cargo.cargo_weight,
                "cargo_volume": c.cargo.cargo_volume,
                "quantity": c.quantity
            })

        return JsonResponse({
            "success": True,
            "data": {
                "order_id": order.order_id,
                "customer_name": order.customer.customer_name,
                "origin_port": order.origin_port,
                "destination_port": order.destination_port,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
                "task": {
                    "task_id": order.task.task_id,
                    "task_status": order.task.task_status
                } if order.task else None,
                "cargos": cargo_list
            }
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
def api_assign_order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer'),
        order_id=order_id
    )

    tasks = Task.objects.select_related('assigned_to').filter(task_status='草稿')

    task_list = []
    for t in tasks:
        task_list.append({
            "task_id": t.task_id,
            "assigned_to": t.assigned_to.username if t.assigned_to else "未指派",
            "origin_port": t.origin_port,
            "destination_port": t.destination_port,
        })

    return JsonResponse({
        "success": True,
        "data": {
            "order": {
                "order_id": order.order_id,
                "customer_name": order.customer.customer_name if order.customer else "",
                "origin_port": order.origin_port,
                "destination_port": order.destination_port,
                "order_status": order.order_status,
            },
            "tasks": task_list
        }
    })
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_assign_order_submit(request, order_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "非法请求"})

    user_info = request.session.get('user_info')
    if not user_info:
        return JsonResponse({"success": False, "message": "未登录"})

    try:
        order = get_object_or_404(Order, order_id=order_id)

        if order.order_status != '待指派':
            return JsonResponse({
                "success": False,
                "message": "该订单不可被指派"
            })

        task_id = request.POST.get('task_id')
        if not task_id:
            return JsonResponse({
                "success": False,
                "message": "请选择任务"
            })

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "任务不存在"
            })

        # ===== 核心逻辑 =====
        order.task = task
        order.order_status = '已指派'
        order.save()

        return JsonResponse({
            "success": True,
            "message": f"订单 {order_id} 已成功指派到任务 {task_id}"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })

from django.core.paginator import Paginator
from django.http import JsonResponse

from django.db.models import Case, When, Value, IntegerField

def api_tasks(request):
    keyword = request.GET.get('keyword', '')
    page = int(request.GET.get('page', 1))

    qs = Task.objects.select_related('assigned_by','assigned_to')

    if keyword:
        qs = qs.filter(task_id__icontains=keyword)

    # ✅ 自定义排序
    qs = qs.order_by(
        Case(
            When(task_status='草稿', then=Value(1)),
            When(task_status='待处理', then=Value(2)),
            When(task_status='运输中', then=Value(3)),
            When(task_status='已完成', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        )
    )

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    data = []
    for t in page_obj:
        data.append({
            "task_id": t.task_id,
            "assigned_by": t.assigned_by.username if t.assigned_by else '',
            "assigned_to": t.assigned_to.username if t.assigned_to else '',
            "assigned_time": t.assigned_time.strftime('%Y-%m-%d %H:%M'),
            "task_status": t.task_status
        })

    return JsonResponse({
        "success": True,
        "data": {
            "list": data,
            "total_pages": paginator.num_pages
        }
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def api_track(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)

    tracks = Track.objects.filter(task=task).order_by('recorded_at')

    data = []
    for i, t in enumerate(tracks, start=1):
        data.append({
            "index": i,
            "latitude": t.latitude,
            "longitude": t.longitude,
            "recorded_at": t.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({
        "success": True,
        "task_id": task.task_id,
        "tracks": data
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def api_task_detail(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)

    orders = task.orders.all().select_related('customer')

    order_list = []
    for o in orders:
        order_list.append({
            "order_id": o.order_id,
            "customer": o.customer.customer_name if o.customer else '',
            "origin_port": o.origin_port,
            "destination_port": o.destination_port,
            "order_status": o.order_status,
            "total_amount": o.total_amount,
            "created_at": o.created_at.strftime('%Y-%m-%d %H:%M')
        })

    data = {
        "task": {
            "task_id": task.task_id,
            "assigned_by": task.assigned_by.username if task.assigned_by else '',
            "assigned_to": task.assigned_to.username if task.assigned_to else '',
            "task_status": task.task_status,
            "origin_port": task.origin_port,
            "destination_port": task.destination_port,
            "assigned_time": task.assigned_time.strftime('%Y-%m-%d %H:%M') if task.assigned_time else '',
            "start_time": task.start_time.strftime('%Y-%m-%d %H:%M') if task.start_time else ''
        },
        "orders": order_list
    }

    return JsonResponse({
        "success": True,
        "data": data
    })

def get_task_detail(request, task_id):
    task = Task.objects.filter(pk=task_id).first()
    if not task:
        return JsonResponse({"error": "任务不存在"}, status=404)

    return JsonResponse({
        "task_id": task.task_id,
        "assigned_to": task.assigned_to.user_id if task.assigned_to else None,
        "origin_port": task.origin_port,
        "destination_port": task.destination_port,
        "start_time": task.start_time.strftime('%Y-%m-%dT%H:%M') if task.start_time else "",
        "task_status": task.task_status
    })



def get_task_meta(request):
    users = User.objects.filter(role_id=4)  # ✅ 只要运输员
    ports = Port.objects.all()

    return JsonResponse({
        "users": [
            {"id": u.user_id, "name": u.username}
            for u in users
        ],
        "ports": [
            {"name": p.port_name}
            for p in ports
        ]
    })
import json

@csrf_exempt
def update_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    task = Task.objects.filter(pk=task_id).first()
    if not task:
        return JsonResponse({"error": "任务不存在"}, status=404)

    data = json.loads(request.body)

    task.assigned_to_id = data.get('assigned_to') or None
    task.origin_port = data.get('origin_port')
    task.destination_port = data.get('destination_port')
    task.start_time = data.get('start_time')
    task.task_status = data.get('task_status')

    task.save()

    return JsonResponse({"success": True})

def get_task_create_meta(request):
    # 只返回“运输员”
    users = User.objects.filter(role__role_name="运输员")

    ports = Port.objects.all()
    orders = Order.objects.filter(order_status='待指派')

    return JsonResponse({
        "users": [
            {"id": u.user_id, "name": u.username}
            for u in users
        ],
        "ports": [
            {
                "name": p.port_name,
                "code": p.port_code,
                "city": p.city,
                "country": p.country
            }
            for p in ports
        ],
        "orders": [
            {
                "id": o.order_id,
                "label": f"{o.order_id} - {o.customer.customer_name}"
            }
            for o in orders
        ]
    })

@csrf_exempt
def create_task_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    user_info = request.session.get('user_info')
    if not user_info:
        return JsonResponse({"error": "未登录"}, status=403)

    data = json.loads(request.body)

    try:
        with transaction.atomic():
            task = Task.objects.create(
                assigned_by_id=user_info['id'],
                assigned_to_id=data.get('assigned_to'),
                assigned_time=timezone.now(),
                task_status=data.get('task_status', '待处理'),
                origin_port=data.get('origin_port'),
                destination_port=data.get('destination_port'),
                start_time=data.get('start_time')
            )

            # 关联订单
            if data.get('order_id'):
                order = Order.objects.get(order_id=data.get('order_id'))
                order.task = task
                order.order_status = '已指派'
                order.save()

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
# views.py
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField

def api_fault_list(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return JsonResponse({"error": "未登录"}, status=401)

    user_id = user_info.get('id')

    fault_reports = (
        FaultReport.objects
        .filter(task_id__assigned_by_id=user_id)
        .select_related('reported_by', 'task_id')
        .annotate(
            status_order=Case(
                When(status='未处理', then=Value(0)),
                When(status='处理中', then=Value(1)),
                When(status='已处理', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        )
        .order_by('status_order')
    )

    data = [{
        "id": f.report_id,
        "task_id": f.task_id.task_id if f.task_id else None,
        "reported_by": f.reported_by.username,
        "reported_at": f.reported_at.strftime('%Y-%m-%d %H:%M'),
        "status": f.status,
        "description": f.description
    } for f in fault_reports]

    return JsonResponse({"faults": data})



@csrf_exempt
def api_fault_detail(request, report_id):
    f = FaultReport.objects.select_related('reported_by', 'task_id').filter(report_id=report_id).first()
    if not f:
        return JsonResponse({"error": "不存在"}, status=404)

    return JsonResponse({
        "id": f.report_id,
        "task_id": f.task_id.task_id if f.task_id else None,
        "reported_by": f.reported_by.username,
        "reported_at": f.reported_at.strftime('%Y-%m-%d %H:%M'),
        "status": f.status,
        "description": f.description
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction

@csrf_exempt
@transaction.atomic
def api_fault_process(request, report_id):
    if request.method != 'POST':
        return JsonResponse({'error': '只允许 POST'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.callproc('handle_fault_report', [report_id])

        return JsonResponse({
            'message': '处理成功',
            'id': report_id
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
    

@csrf_exempt
@transaction.atomic
def api_fault_finish(request, report_id):
    if request.method != 'POST':
        return JsonResponse({'error': '只允许 POST'}, status=405)

    try:
        with connection.cursor() as cursor:
            cursor.callproc('handle_fault_report', [report_id])
            # ⚠️ 如果你没有这个存储过程，可以先继续用 handle_fault_report

        return JsonResponse({
            'message': '已完成',
            'id': report_id
        })

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)