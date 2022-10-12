from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from django.http import HttpResponse


@login_required
def confirmView(request):

	# Note that this transfer is very naive
	# but will suffice for this exercise
	amount = request.session['amount']
	to = User.objects.get(username=request.session['to'])
	if amount >= 0 and amount <= request.user.account.balance:
		request.user.account.balance -= amount
		to.account.balance += amount

		request.user.account.save()
		to.account.save()
	
	return redirect('/')
	
 
@login_required
def transferView(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = int(request.GET.get('amount'))
	return render(request, 'pages/confirm.html')

@login_required
def homepageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts}) 

def signinView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        account = Account(user=user, balance=100)
        account.save()
        return redirect('/')

    return render(request, 'pages/signin.html')

  