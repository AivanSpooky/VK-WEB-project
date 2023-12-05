from app.models import Question, Answer

# Получаем все вопросы из базы данных
all_questions = Question.objects.all()

# Для каждого вопроса обновляем переменную answer_cnt на основе количества ответов
for question in all_questions:
    print(question.title)
    answer_count = Answer.objects.filter(question=question).count()
    question.answer_cnt = answer_count
    question.save()
