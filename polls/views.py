from django.http import HttpResponse,HttpResponseRedirect
#from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def index(request):
    return HttpResponse("Hello, world. You're at the polss index.")
# Create your views here.

def index(request):
    #latest_question_list=Question.objects.order_by('-pub_date')[:5]
    latest_question_list=Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context={
        'latest_question_list':latest_question_list
    }
    #return HttpResponse(template.render(context,request))
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    try:
        question= Question.objects.get(pk=question_id,pub_date__lte=timezone.now())
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    question=get_object_or_404(Question,pk=question_id)
    #question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/details.html',{
            'question':question,
            'error_message':"You did not select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))