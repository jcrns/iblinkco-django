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
from service.models import JobPost, MilestoneFiles

# Importing job form for form updates in detail views
from service.forms import JobPostFormUpdate, milestoneUpdate

# Importing Complete Profile
from users.forms import ProfileUpdateFormClient, ProfileUpdateFormManager

# Getting user evaluation modal
from management.models import ManagerEvaluation

# Importing datetime
from datetime import datetime, timezone

from django.http import HttpResponse

# Importing stripe
import stripe

# Overview function
@login_required(login_url="/?login=true")
def dashboard(request):
    # Getting user
    profile = request.user.profile
    if profile.is_client == False and profile.is_manager == False:
        return redirect('homepage-overview')
    
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
            return redirect('service-complete-profile-client')
    # If manager
    else:
        # Checking if profile is completed
        if profile.description != 'none':

            # Getting evaluation
            evaluation = ManagerEvaluation.objects.get(manager=request.user)

            # Checking if evaluation is completed
            if evaluation.accepted == True:
            
                # Get jobs involved
                update_profile_form = ProfileUpdateFormManager(instance=request.user.profile)
                past_jobs = JobPost.objects.filter(manager=request.user.pk, job_complete=True).order_by('-date_requested')
                current_jobs = JobPost.objects.filter(manager=request.user.pk, job_complete=False).order_by('-date_requested')
                print('profile.stripe_user_id')

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

            # Manager is not evaluated so redirecting to evaluation
            else:
                return redirect('management-evaluation')
        else:
            return redirect('service-complete-profile-manager')
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
    # template_name = 'dashboard/job_detail.html'

    # Overriding the get function to redirect user if not involved in detailed post
    def get(self, request, *args, **kwargs):
        # Getting object
        self.object = self.get_object() 
        user = request.user

        # Checking if user is manager
        if self.template_name == 'dashboard/job_detail_manager.html':
            if user.profile.is_client == True:
                return redirect('dashboard-job-detail-manager', pk=self.object.pk)


        # Checking if user is client 
        if self.template_name == 'dashboard/job_detail_client.html':
            if user.profile.is_manager == True:
                return redirect('dashboard-job-detail-manager', pk=self.object.pk)


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
        client_name = context['object'].client
        
        # Creating time left for job preparation
        jobPrepDeadline = context['object'].job_preparation_deadline
        now = datetime.now(timezone.utc)
        jobPrepTimeLeft = jobPrepDeadline - now
        jobPrepTimeLeft = jobPrepTimeLeft.total_seconds()
        
        jobPrepMinLeft = jobPrepTimeLeft/60
        JobPrepHourLeft = jobPrepMinLeft/60

        JobPrepDaysRemaining = JobPrepHourLeft/24
        JobPrepHoursRemaining = JobPrepHourLeft/24

        if JobPrepDaysRemaining < 1:
            JobPrepTimeLeftStr = str(round(JobPrepHoursRemaining)) + " hours left"
        else:
            # Checking for certain situations
            daysString = " Days left and "
            if int(JobPrepDaysRemaining) == 1:
                daysString = " Day left and "

            hoursString = " hours left"
            if round(JobPrepHoursRemaining) == 1:
                hoursString = " hour left"

            JobPrepTimeLeftStr = str(int(
                JobPrepDaysRemaining)) + daysString + str(round(JobPrepHoursRemaining)) + hoursString

        # Getting profiles and checking if user is assigned
        if manager_name:
            manager_profile = Profile.objects.get(user=manager_name)
        else:
            manager_profile = None
        client_profile = Profile.objects.get(user=client_name)
        
        # Defining and saving form to context
        form = milestoneUpdate()
        context['form'] = form
        
        # Getting img files
        image_list_milestone_one = MilestoneFiles.objects.filter(
            job=context['object'], milestoneOne=True)

        image_list_milestone_two = MilestoneFiles.objects.filter(
            job=context['object'], milestoneTwo=True)
        
        image_list_milestone_three = MilestoneFiles.objects.filter(
            job=context['object'], milestoneThree=True)
        
        image_list_milestone_four = MilestoneFiles.objects.filter(
                job=context['object'], milestoneFour=True)

        # Applying milestone images
        context['image_list_milestone_one'] = image_list_milestone_one
        context['image_list_milestone_two'] = image_list_milestone_two
        context['image_list_milestone_three'] = image_list_milestone_three
        context['image_list_milestone_four'] = image_list_milestone_four


        # Applying found data to context
        context['manager_profile'] = manager_profile
        context['client_profile'] = client_profile

        # Applying additional info
        context['job_prep_days_left'] = JobPrepTimeLeftStr

        # Adding additional context for styling
        context['static_header'] = True
        context['nav_black_link'] = True

        # Adding edit profile form
        context['edit_job_form'] = JobPostFormUpdate(instance=context['object'])

        return context

    # Func for when job form is posted
    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        
        # Getting form with requested data
        form = milestoneUpdate(self.request.POST, self.request.FILES, instance=self.object)
        
        # Getting job for job complete bool update
        job = JobPost.objects.get(pk=self.object.pk)

        # Checking if form is valid
        if form.is_valid():
            
            # Getting inputed statements
            milestone_one_statement = form.cleaned_data.get('milestone_one_statement')
            milestone_two_statement = form.cleaned_data.get(
                'milestone_two_statement')
            milestone_three_statement = form.cleaned_data.get(
                'milestone_three_statement')
            milestone_four_statement = form.cleaned_data.get(
                'milestone_four_statement')

            # Checking which milestone is being updated
            if milestone_one_statement:
                # Getting different images
                for field in self.request.FILES.keys():
                    for formfile in self.request.FILES.getlist(field):
                        # Saving images in the db
                        MilestoneFiles.objects.create(
                            job=self.object, milestoneFile=formfile, milestoneOne=True)

                form.completed_milestone_one = True
                form.save()

            elif milestone_two_statement:
                for field in self.request.FILES.keys():
                    for formfile in self.request.FILES.getlist(field):
                        # Saving images in the db
                        MilestoneFiles.objects.create(
                            job=self.object, milestoneFile=formfile, milestoneTwo=True)

                form.completed_milestone_two = True
                form.save()

            elif milestone_three_statement:
                for field in self.request.FILES.keys():
                    for formfile in self.request.FILES.getlist(field):
                        # Saving images in the db
                        MilestoneFiles.objects.create(
                            job=self.object, milestoneFile=formfile, milestoneThree=True)

                form.completed_milestone_three = True
                form.save()

            elif milestone_four_statement:
                for field in self.request.FILES.keys():
                    for formfile in self.request.FILES.getlist(field):
                        # Saving images in the db
                        MilestoneFiles.objects.create(
                            job=self.object, milestoneFile=formfile, milestoneFour=True)

                form.completed_milestone_four = True
                form.save()

                # Changing job complete bool
                job.job_complete = True
                job.save()

                # Paying managers with stripe
                stripe.Transfer.create(
                    amount=job.manager_payment,
                    currency="usd",
                    destination="acct_1EF7fHDyI4HAPojy",
                )
                

        # # Getting posted data
        # print(self.request.POST)
        # print(self.request.FILES.keys())
        # milestoneNumber = int(self.request.POST['milestone-number'])
        # milestoneDescription = self.request.POST['milestone-description']
        # milestoneFiles = self.request.FILES['milestone-files']
        # print(milestoneFiles)
        # print(milestoneNumber)
        # if not milestoneDescription:
        #     print('milestone description empty')
        #     return redirect('dashboard-job-detail-manager', pk=self.object.pk)
        return redirect('dashboard-job-detail-manager', pk=self.object.pk)

class ConfirmJobDetailView(DetailView):
    model = JobPost
    context_object_name = 'order'
    template_name = 'dashboard/confirm_job.html'
    
    # Overriding the get function to redirect user if not involved in detailed post
    def get(self, request, *args, **kwargs):
        
        # Getting object
        self.object = self.get_object() 
        user = request.user

        if self.object.paid_for == False:
            # Checking if user is either manager or client
            if user == self.object.client or user == self.object.manager:
                # Returning super
                return super(ConfirmJobDetailView, self).get(request, *args, **kwargs)
        # Returning if conditions aren't satisfied
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

# Func to change job prep bool
def jobPrepEnded(request, pk):
    # Getting job
    job = get_object_or_404(JobPost, pk=pk)

    # Defining user
    user = request.user

    # Changing variable in db
    job.job_preparation_completed = True
    job.save()
    return redirect('dashboard-job-detail-manager', pk=pk)
