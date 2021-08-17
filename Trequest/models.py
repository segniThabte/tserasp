from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.http import request
from ckeditor.fields import RichTextField
from TSERASP import settings
from datetime import date

# defining the users school name
class School(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

# defining the users department


class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, blank=True)
    ROLE = (
        ('Passenger', 'Passenger'),
        ('TSHO', 'TSHO'),
        ('Mechanic', 'Mechanic'),
        ('Driver', 'Driver'),
        ('StoreManager', 'Store Manager'),
        ('SchoolDean', 'School Dean'),
        ('DepartmentHead', 'Department Head'),
        ('VicePresident', 'Vice President'),
    )
    # School = (
    #     ('SOEEC', 'SOEEC'),
    #     ('SOMCME', 'SOMCME'),
    #     ('SOCEA', 'SOCEA'),
    #     ('SOANS', 'SOANS'),
    # )
    # Department = (
    #     ('CSE', 'CSE'),
    #     ('ECE', 'ECE'),
    #     ('EPCE', 'EPCE'),
    #     ('MCE', 'MCE'),
    #     ('MSE', 'MSE'),
    #     ('CHE', 'CHE'),
    #     ('CE', 'CE'),
    #     ('WRE', 'WRE'),
    #     ('ARCH', 'ARCH'),
    #     ('Maths', 'Maths'),
    #     ('Pysics', 'Pysics'),
    #     ('Chemistry', 'Chemistry'),
    #     ('Bio', 'Bio'),
    #     ('Geology', 'Geology')
    # )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 0987654321 or +251987654321 up to 15 digits allowed'
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=15, blank=True)
    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.CharField(max_length=200, choices=ROLE)
    date_registered = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username
    # mobile_number = models.CharField(max_length=10, unique=True)
    # birth_date = models.DateField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passenger')
    sex = models.CharField(max_length=200, choices=(
        ('male', 'male'), ('female', 'female')), null=True,blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')
    occupation = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=100, null=True)
    house_no = models.CharField(max_length=100, null=True)

    def __str__(self):
         return self.user.first_name + "  " + self.user.last_name


class TransportRequest(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Expired', 'Expired'),
        
    )
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_request')
    start_from = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    reason = RichTextField(blank=True, null=True)
    passenger_numbers = models.PositiveIntegerField(default=1)
    list_of_passengers = models.TextField(max_length=400, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    # is_expired = models.BooleanField(default=False)
    status = models.CharField(max_length=200, default='Pending', choices=STATUS)
    status2 = models.CharField(max_length=200, default='Pending', choices=STATUS)
    status3 = models.CharField(max_length=200, default='Pending', choices=STATUS)
# status=TSHO
# status2=department
# status3=School

    def __str__(self):
        return self.start_from + ' to ' + self.destination

    class Meta:
        ordering = ['-id']

# to expire the request
# method 1
    @property
    def is_expired(self):
        if date.today() >= self.start_date:
            return True
        return False

# method 2
    # def expire(self):
    #  if datetime.now() >= self.start_date:
    #     self.is_expired = True
    #     return True
    #  else:
    #     return False

# notifications for viewing new request


class Notifications(models.Model):
    # sender_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    request_id = models.ForeignKey(
        TransportRequest, on_delete=models.CASCADE, related_name='trequest')
    is_viewed = models.BooleanField(default=False)
    from_who = models.ForeignKey(
        TransportRequest, on_delete=models.CASCADE, null=True, related_name='from_who')

    def __str__(self):
        return str(self.request_id.passenger.first_name)
    # to dynamically determine vehicle type
    
class VehicleType(models.Model):
    name=models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    STATUS = (
        ('Not Occupied', 'Not Occupied'),
        ('Occupied', 'Occupied'),
    )
    current = (
        ('Outside', 'Outside'),
        ('Inside', 'Inside'),
    )
    # type_of_vehicle = (
    #     ('minibus', 'minibus'),
    #     ('bus', 'bus'),
    #     ('kobra', 'kobra'),
    #     ('ambulance', 'ambulance')
    # )
    adder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='add')
    vehicle_type = models.ForeignKey(VehicleType,on_delete=models.CASCADE)
    adder = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='add')
    plate_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=200, choices=STATUS, default='Not Occupied')
    driver = models.OneToOneField(
        Driver, on_delete=models.CASCADE, null=True, blank=True)
    date_entered = models.DateTimeField(auto_now_add=True, null=True)
    currently = models.CharField(
        max_length=200, choices=current, default='Inside')

    def __str__(self):
        return self.plate_number


class ApproveRequest(models.Model):
    user = models.OneToOneField(TransportRequest, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    time = models.CharField(max_length=200, default='06:00am')

    def __str__(self):
        return self.user.start_from + ' to ' + self.user.destination + ' Approved '


class Schedule(models.Model):
    select = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adder')
    shift = models.CharField(max_length=100, choices=select)
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name='driver_name')
    service_type = models.CharField(max_length=200)
    date = models.DateField()
    time = models.CharField(max_length=200)
    place = models.CharField(max_length=200)

    def __str__(self):
        return self.service_type
#     by naol


class Material(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    type_of = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    date_created = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class MaterialRequest(models.Model):
    # material name
    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete= models.SET_NULL)
    new_material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING, null=True, related_name='new_material')
    new_material_model = models.CharField(max_length=200)
    quantity_of_new = models.PositiveIntegerField()
    # old_material_name = models.ForeignKey(Material, on_delete=models.DO_NOTHING, null=True, related_name='old_material')
    quantity_of_old=models.PositiveIntegerField()
    old_material_model=models.CharField(max_length=200)
    vehicle_model = models.ForeignKey(Vehicle, max_length=200, on_delete=models.DO_NOTHING, null=True)
    condition = models.CharField(max_length=200,choices=(('Reusable', 'reusable'), ('Usable', 'usable')), null=True)
    status = models.CharField(max_length=200, default='Pending', choices=STATUS)


    def __str__(self):
        return self.new_material_name.name
# evaluate Driver


class DriverEvaluation(models.Model):
    select = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),

    )
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name='drivers_name')
    rating = models.CharField(max_length=1, choices=select)
    duser = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='evaluator')
    trip = models.ForeignKey(
        TransportRequest, on_delete=models.CASCADE, related_name='trip_name', null=True)


# feedback
class feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True)
# Activity Log
class ActivityLog(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(max_length=100)
    instances=models.CharField(max_length=500)
    log_object=models.CharField(max_length=100,null=True)
    action=models.CharField(max_length=100,null=True)

# class Material(models.Model):
#     user = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='matregister')
#     name=models.CharField(max_length=200)
#     type = models.CharField(max_length=200)
#     quantity=models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
# # class Schedule(models.Model):
# #     service_type=models.CharField(max_length=)
# #
# # class ReassignSchedule(models.Model):
# #     re_assigned_to=models.ForeignKey(Schedule,on_delete=models.CASCADE)
# class MaterialRequest(models.Model):
#     STATUS = (('Pending','Pending'),
#             ('Approved','Approved'),)
#     user=models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='matrequest')
#     name = models.CharField(max_length=200)
#     type = models.CharField(max_length=200)
#     quantity = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=200, choices=STATUS, default='Pending')
#
#     def __str__(self):
#         return self.name
# # class RepairedVehicle(models.Model):
# # class Profile(models.Model):
# # class Evaluation(models.Model):
