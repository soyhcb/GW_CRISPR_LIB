from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, QueryDict
from general.forms import LoginForm
# Create your views here.
def index(request):
    return HttpResponseRedirect("/crispr_lib")
    # return render(request, "pages/static/index.html")

# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/static/' + load_template)
        return HttpResponse(template.render(context, request))

    except:
        raise Http404

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', '')
                if not next:
                    next = "/"
                return redirect(next)
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "pages/dynamic/auth.html", {"form": form, "msg" : msg})