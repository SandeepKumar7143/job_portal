from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from accounts.models import Profile

@login_required
def job_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all().order_by('-created_at')

    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = Application.objects.filter(
        job=job, applicant=request.user
    ).exists()

    return render(request, 'job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    profile = Profile.objects.get(user=request.user)
    if profile.role != 'seeker':
        messages.error(request, "Only job seekers can apply")
        return redirect('job_detail', job_id=job.id)

    Application.objects.get_or_create(
        job=job,
        applicant=request.user
    )
    messages.success(request, "Job applied successfully")
    return redirect('job_detail', job_id=job.id)


@login_required
def recruiter_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role != 'recruiter':
        messages.error(request, "Access denied")
        return redirect('job_list')

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, 'recruiter_dashboard.html', {'jobs': jobs})


@login_required
def post_job(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role != 'recruiter':
        messages.error(request, "Only recruiters can post jobs")
        return redirect('job_list')

    if request.method == 'POST':
        Job.objects.create(
            recruiter=request.user,
            title=request.POST['title'],
            company=request.POST['company'],
            location=request.POST['location'],
            salary=request.POST['salary'],
            description=request.POST['description']
        )
        messages.success(request, "Job posted successfully")
        return redirect('recruiter_dashboard')

    return render(request, 'post_job.html')


@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job)

    return render(request, 'applicants.html', {
        'job': job,
        'applications': applications
    })

