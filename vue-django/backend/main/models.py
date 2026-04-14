from django.db import models

# Create your models here.

class Permission(models.Model):
    perm_id=models.AutoField(primary_key=True)
    perm_name=models.CharField(max_length=50)
    class Meta:
        db_table='permission'  

class Role(models.Model):
    role_id=models.AutoField(primary_key=True)
    role_name=models.CharField(max_length=50)
    class Meta:
        db_table='role'

class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=255)
    role=models.ForeignKey(Role, on_delete=models.SET_NULL,to_field='role_id',null=True)
    phone=models.CharField(max_length=11)
    email=models.CharField(max_length=50)
    photo=models.CharField(max_length=255,null=True)
    status=models.CharField(max_length=20)
    create_time=models.DateTimeField()
    login_status=models.BooleanField()
    last_visit=models.DateTimeField(null=True)
    class Meta:
        db_table='user'
    

class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=5)
    customer_phone=models.CharField(max_length=11)
    customer_address=models.CharField(max_length=200)
    customer_email=models.CharField(max_length=200,null=True)
    class Meta:
        db_table='customer'


class Port(models.Model):
    port_id = models.AutoField(primary_key=True)
    port_code = models.CharField(max_length=20)
    port_name = models.CharField(max_length=100)
    port_name_en = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'port'

class Cargo(models.Model):
    cargo_id = models.AutoField(primary_key=True)
    cargo_name = models.CharField(max_length=200)
    cargo_type = models.CharField(max_length=100)
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    cargo_volume = models.DecimalField(max_digits=10, decimal_places=3,null=True)
    cargo_amount = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'cargo'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        to_field='user_id', 
        db_column='created_by'
    )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        to_field='customer_id',
        db_column='customer_id',
        null=True, 
        blank=True
    )
    origin_port = models.CharField(max_length=200, null=True, blank=True)
    destination_port = models.CharField(max_length=200, null=True, blank=True)
    order_status = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE, 
        to_field='task_id',
        db_column='task_id',
        related_name='orders',
        null=True,
        blank=True 
    )

    class Meta:
        db_table = 'orders'



class OrderCargo(models.Model):
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE, db_column='cargo_id')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='order_id')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_cargo'
        unique_together = (('cargo', 'order'),)  # 联合主键（货物ID + 订单ID）

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    assigned_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        to_field='user_id', 
        db_column='assigned_by', 
        null=True, 
        blank=True,
        related_name='assigned_tasks'  # 修改反向访问器为 'assigned_tasks'
    )
    assigned_to = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        to_field='user_id', 
        db_column='assigned_to', 
        null=True, 
        blank=True,
        related_name='received_tasks'  # 修改反向访问器为 'received_tasks'
    ) 
    assigned_time = models.DateTimeField()
    task_status = models.CharField(max_length=20)
    origin_port = models.CharField(max_length=200, null=True, blank=True)  # 始发港口
    destination_port = models.CharField(max_length=200, null=True, blank=True)  # 目的港口
    start_time = models.DateTimeField(null=True, blank=True)  # 新增任务开始时间字段

    class Meta:
        db_table = 'tasks'

class Track(models.Model):
    track_id = models.AutoField(primary_key=True)  # 跟踪ID，自增
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        to_field='task_id',
        db_column='task_id',
        related_name='tracks'
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=False)
    recorded_at = models.DateTimeField()

    class Meta:
        db_table = 'track'

class FaultReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(
        'Task', 
        on_delete=models.CASCADE, 
        to_field='task_id', 
        db_column='task_id', 
        related_name='fault_reports'
    )
    reported_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        to_field='user_id', 
        db_column='reported_by', 
        null=True,
        related_name='reported_faults'
    )
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20) 

    class Meta:
        db_table = 'fault_report'

class Role_Permission(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='perm_id')

    class Meta:
        db_table = 'role_permission'
        unique_together = (('role', 'permission'),)
