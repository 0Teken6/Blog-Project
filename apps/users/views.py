from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import UserUpdateForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.contrib.auth import get_user_model


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


class UserProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    

    def get_object(self):
        profile = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
        return profile