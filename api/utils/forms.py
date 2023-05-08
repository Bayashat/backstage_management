from django import forms
from django.core.exceptions import ValidationError

from api.models import EmployeeInfo, Department, Admin, Order, User

from api.utils.bootstrap import BootStrapModelForm, BootStrapForm
from api.utils.encrypt import md5


class DepartModelForm(BootStrapModelForm):

    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop to find all plugins, add class="form-control" and placeholder
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}


class StaffModelForm(BootStrapModelForm):
    # Rewrite custom verification conditions (similar to limit length, etc.)
    first_name = forms.CharField(label="first_name", min_length=3, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="last_name", min_length=3, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = EmployeeInfo
        fields = ['first_name', 'last_name', 'age', 'gender',
                  'account', 'entry_time', 'depart']  # Fields to display

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop to find all plugins, add class="form-control" and placeholder
        for name, field in self.fields.items():
            if name == 'entry_time':
                field.widget.input_type = 'date'
            # print(name, field)
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}


class AdminModelForm(BootStrapModelForm):
    # Define a new field to confirm the password
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)  # Add render_value to not clear data after submit
    )

    class Meta:
        model = Admin
        fields = ["first_name", "last_name", "username", "password", "confirm_password"]
        widgets = {  # Also add to the password input box
            "password": forms.PasswordInput(render_value=True)  # Add render_value to not clear data after submit
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")  # Get password
        return md5(pwd)  # md5 encrypted password

    def clean_confirm_password(self):  # The hook function is used to prompt "inconsistent" Error
        pwd = self.cleaned_data.get("password")  # The password obtained at this time is already encrypted
        confirm = md5(self.cleaned_data.get("confirm_password"))  # The confirmation password is also encrypted
        if confirm != pwd:
            raise ValidationError("The passwords do not match")

        # What to return, this field will be saved to the data later
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['first_name', 'last_name', 'username']


class AdminResetModelForm(BootStrapModelForm):
    # Define a new field to confirm the password
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(render_value=True)  #
    )

    class Meta:
        model = Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)   # Add render_value to hide the password (***), and the data will not be cleared after submit
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")  # Get Password
        md5_pwd = md5(pwd)

        # Go to the database to check whether the current password is consistent with the newly entered password
        is_exist = Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if is_exist:
            raise ValidationError("The password cannot be the same as the previous one")
        return md5(pwd)  # md5 encrypted password

    def clean_confirm_password(self):  # The hook function is used to prompt "inconsistent" Error
        pwd = self.cleaned_data.get("password")  # The password obtained at this time is already encrypted
        confirm = md5(self.cleaned_data.get("confirm_password"))  # The confirmation password is also encrypted
        if confirm != pwd:
            raise ValidationError("The passwords do not match")

        # What to return, this field will be saved to the data later
        return confirm


class LoginForm(BootStrapForm):
    username = forms.CharField(label="username", widget=forms.TextInput)
    password = forms.CharField(label="password", widget=forms.PasswordInput(render_value=True))  # reder_value for don't clear data after submit
    code = forms.CharField(label="verification code", widget=forms.TextInput)

    #   Hook function: used to encrypt password with md5
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class UserModelForm(BootStrapModelForm):
    # Rewrite custom verification conditions (similar to limit length, etc.)
    first_name = forms.CharField(label="first_name", min_length=3, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="last_name", min_length=3, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop to find all plugins, add class="form-control" and placeholder
        for name, field in self.fields.items():
            if name == 'create_time':
                field.widget.input_type = 'date'
            # print(name, field)
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        # fields = "__all__"
        exclude = ['oid']

