
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.template import loader
from .models import Choice, Question, UserProfileInfo, Vote
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from pdb import set_trace
import pandas as pd




def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'polls/login.html', {'response':'Invalid password or username',})
    else:
        return render(request, 'polls/login.html')

@login_required
def profileview(request):

    votes_list = Vote.objects.filter(Voter_username=request.user.username).order_by('question_id')[:5]


    #num_questions = Vote.objects.annotate(num=Count('question'))
    return render(request, 'polls/myprofile.html', {'votes_list':votes_list,})

@login_required
def detailVoteView(request):
    user = request.user.username


@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:index'))

@login_required
def allvotesview(request):
    user=request.user.username
    votes_list = Vote.objects.filter(Voter_username=request.user.username).order_by('question_id')




def RegistrationView(request):
    #template = loader.get_template('polls/registration.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('polls:index')
    else:
        form = UserForm()
    return render(request, 'polls/registration.html',{'User_Form': form,} )




class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'


    def showtotal(self):
        votos = Question.total_votes(self)
        return votos

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        return latest_question_list




class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



@login_required
def vote(request, question_id):
    #set_trace()

    voter=request.user.username
    #print(voter)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        """had_voted = list(Vote.objects.filter(Voter_username=voter))

        if had_voted != None:
            if had_voted.index(question.question_text):
                q = Vote.objects.filter(question.question_text)
                q.num_votes = q.num_votes + 1
        else:"""
        v = Vote.objects.create(Voter_username=voter, choice=selected_choice, question=question, num_votes=1)
        selected_choice.votes = selected_choice.votes + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #return redirect('polls:results', question_id)
