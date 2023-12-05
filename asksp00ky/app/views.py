from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question, Profile, Tag
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Question, Profile, Tag, Like, Answer
import re
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

# ВСЕ ТЕСТЫ ВЫПОЛНЯЛИСЬ НА ПОСЛЕДНЕМ ЮЗЕРЕ
# login: test-user
# password: 958ivan77
profile = Profile.objects.get(id=10000)
logged_in = True

def handle_invalid_page(request):
    return HttpResponse("Page Timed Out. Please inform the user that you could not retrieve the page.")

def user_logout(request):
    global logged_in
    logged_in = False
    return redirect(request.META.get('HTTP_REFERER', '/'))

def login_window(request):
    global logged_in, profile
    error_messages = [message.message for message in messages.get_messages(request)]
    if error_messages:
        error_message = error_messages[0]
        color = error_messages[1]
    else:
        error_message = ''
        color = 'red'

    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        color = "red"
        if user is not None:
            logged_in = True
            login(request, user)
            profile = Profile.objects.get(user=user)
            continue_url = request.GET.get('continue', '/')
            # return HttpResponseRedirect(reverse('index'))  # Перенаправление на главную страницу после успешной авторизации
            return redirect(continue_url)
        else:
            logged_in = False
            error_message = 'Неправильное имя пользователя или пароль.'
            return render(request, 'login.html', {'profile': profile, "log": logged_in, 'error_message': error_message, 'color': color, 'popular_tags': Tag.get_popular_tags()})
    else:
        return render(request, 'login.html', {'profile': profile, "log": logged_in, 'error_message': error_message, 'color': color, 'popular_tags': Tag.get_popular_tags()})

def index(request):
    global logged_in, profile
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(Question.objects.sort_questions(), page, 10)
    return render(request, 'questions.html', {'notag': True, 'questions': paginated_questions, 'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags(),})

def user_registration(request):
    global logged_in, profile
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        email = request.POST['email']
        nickname = request.POST['nickname']
        repeat_password = request.POST['repeat_password']
        avatar = request.FILES.get('avatar')

        # Добавьте здесь обработку ошибок, например:
        error_message = ""
        color = "red"
        if User.objects.filter(username=username).exists():
            error_message = 'Логин уже существует в базе данных.'
            return render(request, 'register.html', {'error_message': error_message, 'popular_tags': Tag.get_popular_tags(), 'profile': profile, "log": logged_in})
        
        if len(nickname) > 30:
            error_message = 'Никнейм не должен превышать 30 символов.'
            return render(request, 'register.html', {'error_message': error_message, 'popular_tags': Tag.get_popular_tags(), 'profile': profile, "log": logged_in})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_message = 'Некорректный формат email.'
            return render(request, 'register.html', {'error_message': error_message, 'popular_tags': Tag.get_popular_tags(), 'profile': profile, "log": logged_in})

        if password != repeat_password:
            error_message = 'Введенный пароль не совпадает с повторенным.'
            return render(request, 'register.html', {'error_message': error_message, 'popular_tags': Tag.get_popular_tags(), 'profile': profile, "log": logged_in})
        
        if not avatar:
            error_message = 'Выберите картинку для аватарки.'
            return render(request, 'register.html', {'error_message': error_message, 'popular_tags': Tag.get_popular_tags(), 'profile': profile, "log": logged_in})

        # Создание пользователя и профиля
        color = "green"
        error_message = "Регистрация прошла успешно! Теперь войдите в свой аккаунт!"
        user = User.objects.create_user(username=username, email=email, password=password)
        profile = Profile(user=user, nickname=nickname, avatar=avatar)
        profile.save()

        # Авторизация пользователя
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, error_message)
            messages.error(request, color)
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'register.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags()})

def settings(request):
    global logged_in, profile
    if request.method == 'POST':
        # Получаем данные из формы редактирования профиля
        new_login = request.POST.get('loginInput')
        new_email = request.POST.get('emailInput')
        new_nickname = request.POST.get('nicknameInput')
        new_avatar = request.FILES.get('avatarFile')

        error_message = None
        color = "red"

        if len(new_nickname) > 30:
            error_message = 'Никнейм не должен превышать 30 символов.'

        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            error_message = 'Некорректный формат email.'

        if error_message:
            return render(request, 'settings.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags(), 'error_message': error_message, 'color': color})
        else:
            # user = request.user
            # if (user.username != new_login):
            #     user.username = new_login
            # user.email = new_email
            # user.save()
            profile.nickname = new_nickname
            if (profile.user.username != new_login):
                profile.user.username = new_login
            profile.user.email = new_email
            if new_avatar:
                profile.avatar = new_avatar
            profile.save()

            success_message = 'Профиль успешно обновлен.'
            color = "green"
            return render(request, 'settings.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags(), 'error_message': success_message, 'color': color})
    else:
        return render(request, 'settings.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags()})

def add_answer(request, question_id):
    global logged_in, profile, question
    if request.method == 'POST':
        if logged_in:  # Проверяем, залогинен ли пользователь
            question_instance  = Question.objects.get(id=question_id) 
            '''get_object_or_404(Question, pk=question_id)'''
            answer_text = request.POST.get('qanswer', '')  # Получаем текст ответа из POST-запроса
            if answer_text:  # Проверяем, что ответ не пустой
                question_instance.answer_cnt += 1
                question_instance.save()
                like_instance = Like(cnt=0)
                like_instance.save()
                dislike_instance = Like(cnt=0)
                dislike_instance.save()
                new_answer = Answer(question=question_instance , author=profile, content=answer_text, like=like_instance, dislike=dislike_instance, correct=False)
                new_answer.save()  # Сохраняем новый ответ в базе данных
                return HttpResponseRedirect(reverse('question', args=(question_id,)))  # Перенаправляем пользователя на страницу вопроса
            else:
                error_message = 'Поле ответа не должно быть пустым!'
                return question(request, question_id, error_message)
        else:
            error_message = 'Вам необходимо залогиниться для добавления ответа!'
            return question(request, question_id, error_message)
    else:
        return question(request, question_id)

def ask(request):
    global logged_in, profile
    all_tags = Tag.objects.all() 
    if request.method == 'POST':
        title = request.POST.get('titleInput')
        content = request.POST.get('contentInput')
        selected_tags = request.POST.getlist('selectedTags')

        error_message = ""
       
        if not logged_in:
            error_message = 'Пожалуйста, войдите в аккаунт.'
        elif not title.strip():
            error_message = 'Пожалуйста, введите заголовок вопроса.'
        elif not content.strip():
            error_message = 'Пожалуйста, введите описание вопроса.'
        elif not selected_tags:
            error_message = 'Пожалуйста, выберите хотя бы один тег.'

        if error_message:
            return render(request, 'ask.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags(), 'error_message': error_message, 'title': title, 'content': content, 'selected_tags': selected_tags, 'all_tags': all_tags})
        else:
            print(f"\n\n{selected_tags}\n\n")
            like_instance = Like(cnt=0)
            like_instance.save()
            dislike_instance = Like(cnt=0)
            dislike_instance.save()
            new_question = Question(title=title, content=content, author=profile, answer_cnt=0, like=like_instance, dislike=dislike_instance)
            new_question.save()

            for tag_id in selected_tags:
                tag = Tag.objects.get(id=tag_id)
                new_question.tags.add(tag) 
            new_question.save()
            print("\n\nadfsads\n\n")
            return HttpResponseRedirect(new_question.get_absolute_url())  # Перенаправляем пользователя на страницу нового вопроса

    else:
        # Если это не POST запрос, просто отображаем форму
        return render(request, 'ask.html', {'profile': profile, "log": logged_in, 'popular_tags': Tag.get_popular_tags(), 'all_tags': all_tags})

def question(request, question_id, error_message=""):
    global logged_in, profile
    question = Question.objects.get(id=question_id)
    page = request.GET.get('page', 1)
    paginated_answers = Question.paginate_questions(question.answer_set.all(), page, 3)
    return render(request, 'question.html', {'question': question, "error_message": error_message, 'answers': paginated_answers, "log": logged_in, 'profile': profile, 'popular_tags': Tag.get_popular_tags(),})

def tag_questions(request, tag):
    global logged_in, profile
    filtered_questions = Question.objects.filter(tags__name=tag)
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(filtered_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": logged_in,
        'p1': f'Tag: {str(tag)} ',
        'profile': profile,
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)

def hot_questions(request):
    global logged_in, profile
    filtered_questions = Question.objects.best_questions()
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(filtered_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": logged_in,
        'p1': 'Hot Questions',
        'profile': profile,
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)

def new_questions(request):
    global logged_in, profile
    new_questions = Question.objects.new_questions()
    page = request.GET.get('page', 1)
    paginated_questions = Question.paginate_questions(new_questions, page, 10)
    context = {
        'questions': paginated_questions,
        'notag': False,
        "log": logged_in,
        'p1': 'New Questions',
        'profile': profile,
        'popular_tags': Tag.get_popular_tags(),
    }
    return render(request, 'questions.html', context)
