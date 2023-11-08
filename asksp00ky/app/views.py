from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator


questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'Long lorem ipsum {i}',
            'likes': 8,
            'answer_cnt': 3,
            'tags': [
                'new',
                'python'
            ],
            'answers': [
                {
                    'id': j+1,
                    'content': "Здесь должен быть текст ответа, но я его пока не придумал))",
                    'likes': 3,
                    'correct': True if (j%2==0) else False 
                } for j in range(3)
            ]
        } for i in range(1000)
    ]

profiles = [
    {
        'id': i,
        'login': 'aivanspooky',
        'password': "1",
        'email': 'IvanSmirnov2002@yandex.ru',
        'nickname': 'sp00ky',
        'avatar': 'img/1.jpeg'
    } for i in range(1)
]

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

def paginate(objects, page, per_page=15):
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page)

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    paginated_questions = paginate(questions, page, 10)
    return render(request, 'questions.html', {'notag': True, 'questions': paginated_questions, 'profile': profiles[profile_id], "log": logged_in})

def login_window(request):
    return render(request, 'login.html', {'profile': profiles[profile_id], "log": logged_in})

def register_window(request):
    return render(request, 'register.html', {'profile': profiles[profile_id], "log": logged_in})

def settings(request):
    return render(request, 'settings.html', {'profile': profiles[profile_id], "log": logged_in})

def ask(request):
    return render(request, 'ask.html', {'profile': profiles[profile_id], "log": logged_in})

def question(request, question_id):
    question = questions[question_id]
    page = request.GET.get('page', 1)
    paginated_answers = paginate(question["answers"], page, 2)
    return render(request, 'question.html', {'question': question, 'answers': paginated_answers, "log": logged_in, 'profile': profiles[profile_id]})

def tag_questions(request, tag):
    filtered_questions = [question for question in questions if tag in question.get('tags', [])]
    context = {
        'questions': filtered_questions,
        'notag': False,
        'p1': f'Tag: {tag} ',
    }
    return render(request, 'questions.html', context)