import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Schoolkid, Lesson, Commendation, \
    Chastisement, Mark


def fix_marks(child):
    """Исправляет все ранее выставленные плохие оценки на оценки 4 и 5"""

    marks = Mark.objects.filter(schoolkid=child).filter(points__lte=3)
    for mark in marks:
        mark.points = random.choice([4, 5])
        mark.save()


def remove_chastisements(child):
    """Удаляет все замечания"""

    Chastisement.objects.filter(schoolkid=child).delete()


def create_commendation(schoolkid_full_name, subject):
    """
    Создает запись похвалы для последнего проведенного урока по указанному
    предмету schoolkid_full_name: имя и фамилия ученика в формате 'Имя Фамилия'
    subject: наименование предмета
    return: None
    """
    commendations = ["Молодец!", "Превосходно!", "Отлично!", ]
    lesson = Lesson.objects.filter(group_letter='А', year_of_study=6,
                                   subject__title=subject).order_by('-date').\
        first()
    if not lesson:
        print('Урок для выставления похвалы не найден')

    try:
        children = Schoolkid.objects.\
            get(full_name__contains=schoolkid_full_name)
    except ObjectDoesNotExist:
        print(f'Ученик с именем {schoolkid_full_name} не найден в базе данных')
        return
    except MultipleObjectsReturned:
        print('Найдено больше одного ученика')
        return

    Commendation.objects.create(text=random.choice(commendations),
                                created=lesson.date, schoolkid=children,
                                subject=lesson.subject, teacher=lesson.teacher)
