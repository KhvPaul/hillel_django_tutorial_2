from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.common import no_append_slash
from django.views.decorators.http import require_http_methods

from .forms import NameForm, QuestionForm, QuestionModelForm
from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


class QuestionResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# @no_append_slash
def current_datetime(request):
    return HttpResponse("Hello")
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    # return render(request, 'polls/detail.html', {'poll': p})


def your_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("polls:index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'polls/form.html', {'form': form})


# def create_question(request):
#     if request.method == "POST":
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = Question.objects.create(
#                 question_text=form.cleaned_data["question_text"], pub_date=datetime.now()
#             )
#             return redirect(reverse("polls:detail", args=(question.id,)))
#     else:
#         form = QuestionForm()
#     return render(request, 'polls/question_form.html', {'form': form})
#
#
# def update_question(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     if request.method == "POST":
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question.question_text = form.cleaned_data["question_text"]
#             question.save()
#             return redirect(reverse("polls:detail", args=(question.id,)))
#     else:
#         form = QuestionForm(initial={"question_text": question.question_text})
#     return render(request, 'polls/question_form.html', {'form': form, "question": question})


def create_question(request):
    if request.method == "POST":
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = datetime.now()
            question.save()
            return redirect(reverse("polls:detail", args=(question.id,)))
    else:
        form = QuestionModelForm(initial={"pub_date": datetime.now()})
    return render(request, 'polls/question_form.html', {'form': form})


def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionModelForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(reverse("polls:detail", args=(question.id,)))
    else:
        form = QuestionModelForm(instance=question)
    return render(request, 'polls/question_form.html', {'form': form, "question": question})
