from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse

#from django.template import loader

from .models import Question, Choice

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list }
    return render(request, "polls/index.html", context)

    # LONGER SOLUTION WITH LOADING TEMPLATE
    # load template
    # template = loader.get_template("polls/index.html")
    # prepare context with variables you will use in your template
    # output = ",".join([q.question_text for q in latest_question_list])
    # render template in HttpResponse
    # return HttpResponse(template.render(context, request))

def detail(request, question_id):
    # shorter and compact version
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question })
    ### Longer version
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    
    return render(request, "polls/detail.html", {"question": question})
    #HttpResponse("You are looking at question %s." % question_id)
    ###

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", { "question": question })
    #response = "You are looking at the results of question %s."
    #return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Re-display the question voting form
        return render(request, "polls/detail.html",
                      {
                          "question": question,
                          "error_message": "You didn't select a choice."
                      })
    else:
        # Avoiding race conditions by using F function
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a user hits
        # the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

    #return HttpResponse("You are voting on question %s." % question_id)