from django.shortcuts import render, redirect

# Lib to require login for certain views
from django.contrib.auth.decorators import login_required

# Importing profile to access 
from users.models import Profile

# Importing jobs to access
from service.models import JobPost

# Importing job form for form updates in detail views
from service.forms import JobPostFormUpdate

# Importing Complete Profile
from users.forms import ProfileUpdateForm

# Importing list view to list past jobs
from django.views.generic import DetailView

# Importing lib to get specific objects
from django.shortcuts import get_object_or_404

# Overview function
@login_required(login_url="/?login=true")
def dashboard(request):
    # Getting user
    profile = request.user.profile

    # Checking if user is client or manager
    if profile.is_client == True:
        if profile.business_type != 'none':
            update_profile_form = ProfileUpdateForm(instance=request.user.profile)
            past_orders = JobPost.objects.filter(client=request.user.pk, job_complete=True).order_by('-date_requested')
            currentJob = JobPost.objects.filter(client=request.user.pk, job_complete=False)

            # Checking if request used post method
            if request.method == 'POST':
                
                # Creating update profile form with post data
                update_profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
                
                # Checking if update profile form is valid
                if update_profile_form.is_valid():
                    profile = update_profile_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect('dashboard-home')
            return render(request, 'dashboard/client.html', { 'profile': profile, 'current_job' : currentJob, 'past_orders' : past_orders, 'update_profile_form' : update_profile_form, "static_header" : True, "nav_black_link" : True } )
        else:
            return redirect('homepage-home')
    else:
        return render(request, 'dashboard/manager.html')

# Adding form to view
def jobDetail(request):
    edit_job_form = JobPostForm()
    
    # When job form is posted
    if request.method == 'POST':
        # Creating update profile form with post data
        edit_job_form = JobPostFormUpdate(request.POST, instance=request.user.profile)

    return render(request, 'dashboard/client.html', edit_job_form)
# Class for displaying info about specific job post
class JobDetailView(DetailView):
    model = JobPost
    context_object_name = 'order'
    template_name = 'dashboard/job_detail.html'

    def custom_save_session(self, request):
        # Getting object
        context = self.get_object() 
        
        # Applying found data to context
        context['manager_profile'] = manager_profile
        context['client_profile'] = client_profile

        # Adding additional context for styling
        context['static_header'] = True
        context['nav_black_link'] = True

        # Adding edit profile form
        context['edit_job_form'] = JobPostFormUpdate(instance=context['object'])

        return context
    # Overriding the get function to redirect user if not involved in detailed post
    def get(self, request, *args, **kwargs):
        # Getting object
        self.object = self.get_object() 
        user = request.user
        print(user)
        print(self.object.client)

        # Checking if user is either manager or client
        if user is self.object.client or user is self.object.manager:
            print('dfef')
            return redirect('dashboard-home')
        return super(JobDetailView, self).get(request, *args, **kwargs)

    # Overriding django function to change context
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)

        # Defining manager and client profiles
        manager_name = context['object'].manager
        manager_profile = Profile.objects.filter(user=manager_name)
        user = self.request.user
        client_profile = self.request.user.profile
        
        # Applying found data to context
        context['manager_profile'] = manager_profile
        context['client_profile'] = client_profile

        # Adding additional context for styling
        context['static_header'] = True
        context['nav_black_link'] = True

        # Adding edit profile form
        context['edit_job_form'] = JobPostFormUpdate(instance=context['object'])

        print(context['object'].pk)
        return context

    # Func for when job form is posted
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        edit_job_form = JobPostFormUpdate(request.POST, instance=self.object)
        if edit_job_form.is_valid():
            edit_job_form.save()
            return redirect('dashboard-job-detail', pk=self.object.pk)
        else:
            return redirect('dashboard-job-detail', pk=self.object.pk)

