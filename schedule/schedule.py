import media

week_days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота', 'Воскресенье']

def create_schedule_day(week_day, url):
    file = open(url, 'r', encoding="UTF-8")
    file_list = file.readlines()
    day_1 = file_list.index(week_days[week_day]+'\n')
    day_2 = file_list.index(week_days[week_day+1]+'\n')
    
    return file_list[day_1:day_2]