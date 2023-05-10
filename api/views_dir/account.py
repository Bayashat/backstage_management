from django import forms
from django.shortcuts import render, redirect, HttpResponse
from io import BytesIO

from api.models import Admin

from api.utils.encrypt import md5
from api.utils.code import check_code
from api.utils.forms import LoginForm


#                   1) Login page
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'account_login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        #  The authentication is successful, the username and password obtained
        # Get Dict: {'username': 'xxxx', 'password': '123456', 'code': 'ABCD'}
        # Get Dict: {'username': 'xxxx', 'password': 'e4271206674ac5032e466cf92ffd7378', 'code': 'ABCD'}
        print(form.cleaned_data)

        #  Check verification code
        user_input_code = form.cleaned_data.pop('code')  # Needs to be removed, because will checked with the database later
        image_code = request.session.get('image_code', '')  # May be empty due to 60 second timeout
        if image_code.upper() != user_input_code.upper():  # incorrect verification code
            form.add_error('code', 'verification code error')
            return render(request, 'account_login.html', {"form": form})

        #  Verify whether the username and password are correct, and get the user object / None
        admin_obj = Admin.objects.filter(**form.cleaned_data).first()  # .filter(username='xxx',password='xxx').first()
        if not admin_obj:
            form.add_error('password', "Username or Password incorrect")
            return render(request, 'account_login.html', {"form": form})

        #   Username and Password Correct
        #   The website generates a random string, write it into the cookie of the user's browser; then write it into the session
        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        #   Now Session can save for 7 days
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('api:admin_list')

    return render(request, 'account_login.html', {"form": form})


def logout(request):
    request.session.clear()     # Clear the currently accessed session
    return redirect('api:login')


def image_code(request):
    """Generate image verification code"""
    # Call the pillow function to generate a picture
    img, code_string = check_code()
    print(code_string)

    # Write code_str to the user session (so that the verification code can be obtained later and then verified)
    request.session['image_code'] = code_string

    # Set the session to time out after 60 seconds, and the picture will be invalid after 60 seconds
    request.session.set_expiry(60)

    stream = BytesIO()  # Create a ByteIO object
    img.save(stream, 'png')  # write into object

    return HttpResponse(stream.getvalue())
