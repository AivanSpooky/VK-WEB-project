from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
import random

content_examples = [
    "Я захотел протестить данный сайт, поэтому ловите мое супер-оригинальное описание вопроса!",
    "Хочу спросить пользователей сайта, меня одного бесит язык Си? Низкоуровневый кусок, на котором микрики максимум из самого непозорного можно сделать... Что думаете по этому поводу?",
    "Появился вопрос для тех, кто шарит за PvP в Minecraft на версии 1.8. Как правильно w-tap-ить? Я просто не понимаю, с каким интервалом нажимать кнопку w..."
]
answer_examples = [
    "Вообще не знаю, что тут ответить. Думаю, тебе стоит переформулировать свой вопрос.",
    "Чел, а ты не пробовал гуглить?",
    "Как тебе объяснить? Вот уже ответили на твой вопрос: https://youtu.be/dQw4w9WgXcQ?si=16-tT9oT6er-Eqb9",
    "Здесь должен быть текст ответа, но я его пока не придумал))"
]

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation (recommended:10000)')

    def handle(self, *args, **options):
        ratio = options['ratio']
        # Create users
        for _ in range(ratio):
            print(f'user-{str(_)}')
            user = User.objects.create(username=f'user-{str(_)}')
            profile = Profile.objects.create(user=user, nickname=f'nickname-{str(_)}', avatar=f'img/avatars/{random.randint(1, 30)}.jpg')

        # Create tags
        for _ in range(ratio):
            print(f'tag-{str(_)}')
            tag = Tag.objects.create(name=f'tag-{str(_)}')

        # Create questions and answers
        for _ in range(ratio * 10):
            print(f'Question-{str(_)}')
            author = Profile.objects.get(id=random.randint(1, ratio))
            like, created = Like.objects.get_or_create(cnt=random.randint(0, 100))
            dislike, created = Like.objects.get_or_create(cnt=random.randint(0, 100))
            question = Question.objects.create(title=f'Question-{str(_)}', content=content_examples[random.randint(0, len(content_examples)-1)], answer_cnt=random.randint(0, 10), author=author, like=like, dislike=dislike)
            tag_nums = set()
            # Define from 1 to 3 tags to each question
            max_tags = 3
            for __ in range(max_tags):
                tag_nums.add(random.randint(1, ratio))
            tag_nums = list(tag_nums)
            for i in range(len(tag_nums)):
                question.tags.add(Tag.objects.get(id=tag_nums[i]))
            for _ in range(10):
                like, created = Like.objects.get_or_create(cnt=random.randint(0, question.like.cnt))
                dislike, created = Like.objects.get_or_create(cnt=random.randint(0, question.dislike.cnt))
                author = Profile.objects.get(id=random.randint(1, ratio))
                answer = Answer.objects.create(content=answer_examples[random.randint(0, len(answer_examples)-1)], correct=bool(random.getrandbits(1)), question=question, like=like, dislike=dislike, author=author)
