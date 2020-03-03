from django.shortcuts import render, redirect, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from apps.second_exam_attempt_app.models import User, Jobs
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt


# Create your views here.


def index(request):

    return render(request, "second_exam_attempt_app/index.html")




def login(request):


    matched_users = User.objects.filter(email=request.POST["email"])

    if matched_users:
        user = matched_users[0]

        pw_matched = bcrypt.checkpw(request.POST['password'].encode(),
                                    user.password.encode())

        if pw_matched:
            request.session['uid'] = user.id
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Try again")
        return redirect("/")
    return redirect("/dashboard")




def register(request):

    if request.POST["password"] != request.POST["password_confirm"]:
        messages.error(request, "Password must match confirm password")

    if len(request.POST["first_name"]) < 2:
        messages.error(request, "First Name must be at least 2 characters!")

    if len(request.POST["last_name"]) < 2:
        messages.error(request, "Last Name must be at least 2 characters")

    if len(request.POST["email"]) < 2:
        messages.error(request, "Email must be at least 2 characters!")

    if len(request.POST["password"]) < 2:
        messages.error(request, "Password must be at least 2 characters")

    if len(request.POST["first_name"]) == 0:
        messages.error(request, "A first name must be provided!")

    if len(request.POST["last_name"]) == 0:
        messages.error(request, "A last name must be provided!")

    if len(request.POST["email"]) == 0:
        messages.error(request, "A email must be provided!")

    if len(request.POST["password"]) == 0:
        messages.error(request, "A password must be provided!")

    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return redirect("/")

    matched_users = User.objects.filter(email=request.POST["email"])

    if matched_users:
        return redirect("/")
    # check if reg valid
    #if not User.objects.is_reg_valid(request):
        #return redirect ("/")

    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    new_user = User.objects.create(first_name=request.POST["first_name"], 
                                    last_name=request.POST["last_name"], 
                                    email=request.POST["email"], 
                                    password=hashed)

    #request.session["uid"] = new_user.id
    return redirect("/dashboard")




def logout(request):
    request.session.clear()
    return redirect('/')




def dashboard(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    user = User.objects.get(id=uid)
    context = {
        "uid": uid,
        "user": user,
        "all_jobs": Jobs.objects.all(),
    }
    return render(request, "second_exam_attempt_app/dashboard.html", context)



def new(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    user = User.objects.get(id=uid)
    context = {
        "user": user,
    }
    return render(request, "second_exam_attempt_app/new.html", context)




def create(request):
    uid = request.session.get("uid")

    if not request.session.get("uid"):
        return redirect("/")

    user = User.objects.get(id=uid)

    if len(request.POST["Title"]) < 3:
        messages.error(request, "A title must consist of at least 3 characters!")
    
    if len(request.POST["Description"]) < 3:
        messages.error(request, "A description must consist of at least 3 characters!")

    if len(request.POST["Location"]) < 3:
        messages.error(request, "A location must consist of at least 3 characters!")

    if len(request.POST["Title"]) == 0:
        messages.error(request, "A title must be provided!")
    
    if len(request.POST["Description"]) == 0:
        messages.error(request, "A description must be provided!")

    if len(request.POST["Location"]) == 0:
        messages.error(request, "A location must be provided!")


    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return redirect("/jobs/new")

    new_job = Jobs.objects.create(job_title=request.POST["Title"], 
                                    job_description=request.POST["Description"],
                                    job_location=request.POST["Location"],
                                    created_by=user)
    
    return redirect("/dashboard")




def remove(request, job_id):

    job_to_delete = Jobs.objects.get(id=job_id)
    job_to_delete.delete()

    return redirect("/dashboard")




def edit_page(request, job_id):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    job_to_edit = Jobs.objects.get(id=job_id)

    user = User.objects.get(id=uid)
    
    context = {
        "job_to_edit": job_to_edit,
        "user": user,
    }
    
    return render(request, "second_exam_attempt_app/edit.html", context)





def edit_process(request, job_id):
    
    uid = request.session.get("uid")

    if not request.session.get("uid"):
        return redirect("/")

    user = User.objects.get(id=uid)

    if len(request.POST["Title"]) < 3:
        messages.error(request, "A title must consist of at least 3 characters!")
    
    if len(request.POST["Description"]) < 3:
        messages.error(request, "A description must consist of at least 3 characters!")

    if len(request.POST["Location"]) < 3:
        messages.error(request, "A location must consist of at least 3 characters!")

    if len(request.POST["Title"]) == 0:
        messages.error(request, "A Title must be provided!")
    
    if len(request.POST["Description"]) == 0:
        messages.error(request, "A description must be provided!")

    if len(request.POST["Location"]) == 0:
        messages.error(request, "A location must be provided!")

    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    job_to_edit = Jobs.objects.get(id=job_id)

    job_to_edit.job_title = request.POST["Title"]
    job_to_edit.job_description = request.POST["Description"]
    job_to_edit.job_location = request.POST["Location"]

    job_to_edit.save()
    
    return redirect("/dashboard")




def view(request, job_id):

    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    job_to_view = Jobs.objects.get(id=job_id)

    user = User.objects.get(id=uid)
    
    context = {
        "job_to_view": job_to_view,
        "user": user,
    }
    
    return render(request, "second_exam_attempt_app/details.html", context)