from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    # to tell django which template to use, default would be <app name>/<model name>_list.html
    # so polls/question_list.html
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions. """
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # Since we are using a model, we do not need to specify explicitly, the name of context variable matches to
    # model name
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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