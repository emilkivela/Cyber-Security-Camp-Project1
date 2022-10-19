from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.http import HttpResponse


@login_required
def confirmView(request):

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
	# CSRF 
	# To fix the CSRF-vulnerability, we need to change the form from GET to POST
	# we also need to do changes to the HTML in index.html
	request.session['to'] = request.GET.get('to') # request.session['to'] = request.POST.get('to')
	request.session['amount'] = int(request.GET.get('amount')) # request.session['amount'] = int(request.POST.get('amount'))
	request.session['message'] = request.GET.get('message') # request.session['message'] = request.POST.get('message')
	Transaction.objects.create(source=request.user, target=User.objects.get(username=request.session['to']), message=request.session['message'], amount=request.session['amount'])
	return render(request, 'pages/confirm.html')

@login_required
def homepageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	transactions = Transaction.objects.filter(source=request.user)

	return render(request, 'pages/index.html', {'accounts': accounts, 'transactions' : transactions}) 
 
@login_required
def transactionView(request):
	transactions = Transaction.objects.filter(source=request.user)
	return render(request, 'pages/transactions.html', {'transactions' : transactions})

def signinView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        account = Account(user=user, balance=100)
        account.save()
        return redirect('/')

    return render(request, 'pages/signin.html')

def infoView(request, transaction_id):
	# Broken Access Control
	# This vulnerability could be fixed by adding line: if transaction.source != request.user: return redirect('/')
	transaction = Transaction.objects.get(id=transaction_id)
	return render(request, 'pages/info.html', {'transaction' : transaction})

