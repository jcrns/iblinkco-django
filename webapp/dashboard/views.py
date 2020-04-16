from django.shortcuts import render, redirect

# Lib to require login for certain views
from django.contrib.auth.decorators import login_required

# Adding mixins
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Importing list view to list past jobs
from django.views.generic import DetailView, DeleteView

# Importing lib to get specific objects
from django.shortcuts import get_object_or_404

# Importing profile to access 
from users.models import Profile

# Importing jobs to access
from service.models import JobPost

# Importing job form for form updates in detail views
from service.forms import JobPostFormUpdate

# Importing Complete Profile
from users.forms import ProfileUpdateFormClient, ProfileUpdateFormManager


# Overview function
@login_required(login_url="/?login=true")
def dashboard(request):
    # Getting user
    profile = request.user.profile
    if profile.is_client == False and profile.is_manager == False:
        return redirect('homepage-home')
    
    # Checking if user is client or manager
    if profile.is_client == True:
        if profile.business_type != 'none':
            update_profile_form = ProfileUpdateFormClient(instance=request.user.profile)
            past_orders = JobPost.objects.filter(client=request.user.pk, job_complete=True).order_by('-date_requested')
            currentJob = JobPost.objects.filter(client=request.user.pk, job_complete=False)

            # Checking if request used post method
            if request.method == 'POST':
                
                # Creating update profile form with post data
                update_profile_form = ProfileUpdateFormClient(request.POST or None, request.FILES or None, instance=request.user.profile)
                
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
        if profile.description != 'none':
            
            # Get jobs involved
            update_profile_form = ProfileUpdateFormManager(instance=request.user.profile)
            past_jobs = JobPost.objects.filter(manager=request.user.pk, job_complete=True).order_by('-date_requested')
            current_jobs = JobPost.objects.filter(manager=request.user.pk, job_complete=False).order_by('-date_requested')
            
            # Checking if request used post method
            if request.method == 'POST':
            
                # Creating update profile form with post data
                update_profile_form = ProfileUpdateFormManager(request.POST or None, request.FILES or None, instance=request.user.profile)
                
                # Checking if update profile form is valid
                if update_profile_form.is_valid():
                    profile = update_profile_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect('dashboard-home')
        else:
            return redirect('homepage-home')
        return render(request, 'dashboard/manager.html', { 'profile': profile, 'current_jobs' : current_jobs, 'past_jobs' : past_jobs, 'update_profile_form' : update_profile_form, "static_header" : True, "nav_black_link" : True })

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

    # Overriding the get function to redirect user if not involved in detailed post
    def get(self, request, *args, **kwargs):
        # Getting object
        self.object = self.get_object() 
        user = request.user

        # Checking if user is either manager or client
        if user == self.object.client or user == self.object.manager:

            # Checking if job is not paid
            if self.object.paid_for == False:
                # Redirecting to confirm screen
                return redirect('dashboard-confirm-job', pk=self.object.pk)

            # Returning super
            return super(JobDetailView, self).get(request, *args, **kwargs)
        else:
            return redirect('dashboard-home')
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

class ConfirmJobDetailView(DetailView):
    model = JobPost
    context_object_name = 'order'
    template_name = 'dashboard/confirm_job.html'
    
    # Overriding the get function to redirect user if not involved in detailed post
    def get(self, request, *args, **kwargs):
        
        # Getting object
        self.object = self.get_object() 
        user = request.user

        # Checking if user is either manager or client
        if user == self.object.client or user == self.object.manager:
            # Returning super
            return super(ConfirmJobDetailView, self).get(request, *args, **kwargs)
        else:
            # Redirecting to dash
            return redirect('dashboard-home')
        

            

    # Overriding django function to change context
    def get_context_data(self, **kwargs):
        context = super(ConfirmJobDetailView, self).get_context_data(**kwargs)

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

# Delete user function
def deleteJob(request, pk):
    # Getting job
    job = get_object_or_404(JobPost, pk=pk)

    # Defining user
    user = request.user

    # Defining profile
    profile = request.user.profile

    # Checking if user is involved in job
    if user == job.client or user == job.manager:
        
        # Deleting job
        job.delete()
        
        # Making user non busy
        profile.busy = False
        profile.save(update_fields=["busy"])
    return redirect('dashboard-home')
