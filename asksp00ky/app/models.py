from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='img/avatars/', default='img/avatars/default.jpg')

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)
    
    @staticmethod
    def get_popular_tags(count=5):
        return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:count]

class Like(models.Model):
    cnt = models.IntegerField(null=0)

class Answer(models.Model):
    content = models.TextField()
    like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='answer_likes')
    dislike = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='answer_dislikes')
    correct = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_total_rating(self):
        return str(int(self.like.cnt - self.dislike.cnt))
    

class QuestionManager(models.Manager):
    def best_questions(self):
        return self.get_queryset().annotate(
            rating=models.F('like__cnt') - models.F('dislike__cnt')
        ).order_by('-rating')[:10]

    def new_questions(self):
        return self.get_queryset().order_by('-id')[:10]
    
    def sort_questions(self):
        return self.get_queryset().order_by('-id')[::-1]

class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='question_likes')
    dislike = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='question_dislikes')
    answer_cnt = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = QuestionManager()

    def get_absolute_url(self):
        return f'/question/{self.id}'
    
    def get_total_rating(self):
        return str(int(self.like.cnt - self.dislike.cnt))

    @staticmethod
    def paginate_questions(objects, page, per_page=15):
        paginator = Paginator(objects, per_page)
        return paginator.get_page(page)