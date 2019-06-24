import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roboot.settings')
import django
django.setup()


from robot_app.models import QA


def read_question():
    question = QA.objects.all().values_list('question')
    question = [i[0] for i in question]
    return question


def read_answer(index):
    answer = QA.objects.all()[index].answer
    return answer


if __name__ == '__main__':
    print(read_question())