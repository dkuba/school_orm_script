from datacenter.models import Schoolkid, Lesson, Commendation, Chastisement, Mark

import random


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
    Создает запись похвалы для последнего проведенного урока по указанному предмету
    schoolkid_full_name: имя и фамилия ученика в формате 'Имя Фамилия'
    subject: наименование предмета
    return: None
    """
    COMMENDATIONS = ["Молодец!", "Превосходно!", "Отлично!", ]
    lesson = Lesson.objects.filter(group_letter='А', year_of_study=6, subject__title=subject).order_by('-date').first()
    if not lesson:
        print('Урок для выставления похвалы не найден')
    childs = Schoolkid.objects.filter(full_name__contains=schoolkid_full_name)
    if childs.count() > 1:
        print('Найдено больше одного ученика')
        return
    elif not childs:
        print(f'Ученик с именем {schoolkid_full_name} не найден в базе данных')
        return
    Commendation.objects.create(text=random.choice(COMMENDATIONS), created=lesson.date, schoolkid=childs[0 ], subject=lesson.subject, teacher=lesson.teacher)
