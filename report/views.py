from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, QueryDict
import json

from report.models import Report
from report.forms import ReportForm

# Create your views here.

def report(request):
    if request.method == "POST":
        return submit_report(request)
    form = ReportForm()
    return render(request, "pages/dynamic/report.html", {"form" : form})
    # return HttpResponse("HelloWorld")

def submit_report(request):
    try:
        f = ReportForm(request.POST)
        f.save()
        return render(request, "pages/static/feedback.html", {'status': True, "info" : "Your report have been successfully submitted! We will check your feedback as soon as possible."})
    except:
        return render(request, "pages/static/feedback.html", {'status': False, "info" : "Something is wrong. Please try it again!"})
