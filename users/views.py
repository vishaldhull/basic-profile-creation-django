from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
# Create your views here.

#registers new user and notify regarding that and redirects them to login page, once registration is successful
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username= form.cleaned_data.get('username')
			messages.success(request, 'Your account has been created! you are now able to log in.')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})

#profile represents all the users our database has, and also repesent which user has been logged in.
@login_required
def profile(request):
	all_users = User.objects.all()
	context = {
        'all_users': all_users
    }
	return render(request, 'users/profile.html', context)

#getUser represents the selected user from dropdown, which will be deleted by current user.
@login_required
def getUser(request):
	results = request.GET['select_user']
	user = User.objects.get(id=results)

	context={
		'select_user': results,
		'user': user 
	}
	return render(request, 'users/delete_selected_user.html', context)

#deleteUser represents the post request of getUser, where it tooks the required 'pk' of user to be deleted and deletes the selected user.
@login_required
def deleteUser(request, pk):
	user = User.objects.get(id=pk)
	if request.method == 'POST':
		user.delete()
		messages.success(request, 'Selected user has been deleted.')
		return redirect('/')

	context = {
		'user':user
	}
	return render(request, 'users/delete_user.html', context)

