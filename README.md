# HW17
# Назначение системы
Система находит наиболее актуальные навыки для какой либо вакансии (hh api)

# Принцип работы системы
Система будет получает данные по вакансиям используя заданные параметры (город, название вакансии). После того как получены описания всех вакансий по заданным параметрам, система производит следующий анализ:
1. Сколько всего вакансий
2. Все требования к данному типу вакансий
3. В скольких вакансиях указано данное требование (сортируем по убыванию)

Последний просмотренный запрос сохраняется на диске в формате json

История всех запросов сохраняется в базе данных
