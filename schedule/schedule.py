from PIL import ImageFont, Image, ImageDraw

week_days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота', 'Воскресенье', '']

def create_schedule_day(week_day, url):
    file = open(url, 'r', encoding="UTF-8")
    file_list = file.readlines()
    day_1 = file_list.index(week_days[week_day]+'\n')
    day_2 = file_list.index(week_days[week_day+1]+'\n')

    return ''.join(file_list[day_1+1:day_2])

def geniration_schedule_image(url_image, url_save, week_day, url_scedule_text):
    text = create_schedule_day(week_day, url_scedule_text).encode('utf-8').decode('utf-8')
    image = Image.open(url_image)
    image_drow = ImageDraw.Draw(image)
    font = ImageFont.truetype("/home/Bananchik/static/fonts/calibri.ttf", 40, encoding='UTF-8')
    image_drow.text((90,140), text, fill="black", align="left", font=font)
    image.save(url_save)
    return url_save