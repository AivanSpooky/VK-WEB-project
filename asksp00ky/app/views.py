from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Profile, Tag
from django.db import models

# from django.core.paginator import Paginator


# questions = [
#         {
#             'id': i,
#             'title': f'Question {i}',
#             'content': f'Long lorem ipsum {i}',
#             'likes': 8,
#             'answer_cnt': 3,
#             'tags': [
#                 'new',
#                 'python'
#             ],
#             'answers': [
#                 {
#                     'id': j+1,
#                     'content': "Здесь должен быть текст ответа, но я его пока не придумал))",
#                     'likes': 3,
#                     'correct': True if (j%2==0) else False 
#                 } for j in range(3)
#             ]
#         } for i in range(1000)
#     ]

# profiles = [
#     {
#         'id': i,
#         'login': 'aivanspooky',
#         'password': "1",
#         'email': 'IvanSmirnov2002@yandex.ru',
#         'nickname': 'sp00ky',
#         'avatar': 'img/1.jpeg'
#     } for i in range(1)
# ]

profile_id = 0
logged_in = True

def handle_invalid_page(request):
    return HttpResponse("Page Timed Out. Please inform the user that you could not retrieve the page.")

def logout(request):
    global logged_in
    logged_in = False
    return redirect(request.META.get('HTTP_REFERER', '/'))

def login_macro(request):
    global logged_in
    logged_in = True
    print(logged_in)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(Question.objects.all(), page, 10)
    return render(request, 'questions.html', {'notag': True, 'questions': paginated_questions, 'profile': Profile.objects.get(id=1), "log": True, 'popular_tags': Tag.get_popular_tags(),})

def login_window(request):
    return render(request, 'login.html', {'profile': Profile.objects.get(id=1), "log": True})

def register_window(request):
    return render(request, 'register.html', {'profile': Profile.objects.get(id=1), "log": True})

def settings(request):
    return render(request, 'settings.html', {'profile': Profile.objects.get(id=1), "log": True})

def ask(request):
    return render(request, 'ask.html', {'profile': Profile.objects.get(id=1), "log": True})

def question(request, question_id):
    question = Question.objects.get(id=question_id)
    page = request.GET.get('page', 1)
    paginated_answers = Question.paginate_questions(question.answer_set.all(), page, 3)
    return render(request, 'question.html', {'question': question, 'answers': paginated_answers, "log": True, 'profile': Profile.objects.get(id=1), 'popular_tags': Tag.get_popular_tags(),})

def tag_questions(request, tag):
    filtered_questions = Question.objects.filter(tags__name=tag)
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(filtered_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": True,
        'p1': f'Tag: {str(tag)} ',
        'profile': Profile.objects.get(id=1),
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)

def hot_questions(request):
    filtered_questions = Question.objects.best_questions()
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(filtered_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": True,
        'p1': 'Hot Questions',
        'profile': Profile.objects.get(id=1),
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)

def new_questions(request):
    new_questions = Question.objects.new_questions()
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(new_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": True,
        'p1': 'New Questions',
        'profile': Profile.objects.get(id=1),
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)

