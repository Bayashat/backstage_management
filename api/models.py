from django.db import models


class Department(models.Model):
    title = models.CharField(verbose_name="Title", max_length=64)

    def __str__(self):
        return self.title


class EmployeeInfo(models.Model):
    first_name = models.CharField(verbose_name="first_name", max_length=128)
    last_name = models.CharField(verbose_name="last_name", max_length=128)
    age = models.IntegerField(verbose_name="Age")

    gender_choices = (
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)

    account = models.DecimalField(verbose_name="Account balance", max_digits=10, decimal_places=2, default=0)

    entry_time = models.DateField(verbose_name="Entry time")

    depart = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=128, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=128, null=True, blank=True)
    username = models.CharField(verbose_name="Username", max_length=64)
    password = models.CharField(verbose_name="Password", max_length=64)

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name}"


class User(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=128, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=128, null=True, blank=True)
    gender_choices = (
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)
    contact_number = models.IntegerField(verbose_name="Contact Number")
    address = models.CharField(verbose_name="Address", max_length=128, null=True, blank=True)
    create_time = models.DateField(verbose_name="Create time", auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


class Order(models.Model):
    oid = models.CharField(verbose_name="Order ID", max_length=128)
    title = models.CharField(verbose_name="Product Name", max_length=32)
    price = models.DecimalField(verbose_name="Product Price", max_digits=10, decimal_places=2, default=None)
    payment_status_choices = (
        (1, 'Pending'),
        (2, 'Completed'),
        (3, 'Failed'),
        (4, 'Refunded'),
        (5, 'Cancelled')
    )
    payment_status = models.SmallIntegerField(verbose_name="Payment Status", choices=payment_status_choices, default=1)

    delivery_status_choices = (
        (1, 'Pending'),
        (2, 'Shipped'),
        (3, 'Delivered'),
        (4, 'Cancelled'),
        (5, 'Returned')
    )
    delivery_status = models.SmallIntegerField(verbose_name="Delivery Status", choices=delivery_status_choices, default=1)

    user = models.ForeignKey(verbose_name="User", to="User", to_field="id", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

