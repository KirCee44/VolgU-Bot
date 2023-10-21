from PIL import ImageFont, Image, ImageDraw
import openpyxl

week_days = ['ПН','ВТ','СР','ЧТ','ПТ','CБ', None]

def create_schedule_day(week_day, url, numenator_denomenator):
    file = openpyxl.open(url, data_only=True)
    file = file['Расписание']
    pair_list = []
    flag = False
    for i in range(2, 87):
        day = file.cell(column=1, row=i).value
        pair = file.cell(column=3, row=i).value
        if week_days.index(day) < week_day or week_days.index(day) > week_day and week_days.index(day) != 6:
            flag = True
        if week_days.index(day) == week_day or week_days.index(day) == 6 and flag == False:
            flag = False
            if pair != None:
                if numenator_denomenator == 0 and i % 2 == 0:
                    pair_list.append('/n')
                    pair_list.append(pair)
                elif numenator_denomenator == 1 and i % 2 != 0:
                    pair_list.append('/n')
                    pair_list.append(pair)
    return ''.join(pair_list)           

def geniration_schedule_image(url_image, url_save, week_day, url_scedule_text, numenator_denomenator):
    x,y = 90, 110
    count_text_max_width = 0
    text_list = []
    text = create_schedule_day(week_day, url_scedule_text, numenator_denomenator).encode('utf-8').decode('utf-8')
    text_list_temp = text.split()
    image = Image.open(url_image)
    image_drow = ImageDraw.Draw(image)
    font = ImageFont.truetype("/home/Bananchik/static/fonts/calibri.ttf", 25, encoding='UTF-8')
    for t in text_list_temp:
        t = t + ' '
        if '/n' in t:
            t = t.replace('/n', '\n')
        if count_text_max_width != 5:
            text_list.append(t)
            if not '\n' in t:
                count_text_max_width += 1
            elif count_text_max_width > 0:
                count_text_max_width -= 1
        else:
            text_list.append('\n')
            text_list.append(t)
            count_text_max_width = 0
    text = ''.join(text_list)
    image_drow.text((x,y), text, fill="black", align="left", font=font)
    image.save(url_save)
    return url_save