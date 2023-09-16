import datetime
import math
def numerator_denominator():
    week_day = datetime.date.today().weekday() + 1
    week = math.ceil((datetime.date.today().day - week_day)/7)
    if week % 2 == 0:
        week_numenator_denomenator = 0
    elif week % 2 != 0:
        week_numenator_denomenator = 1
    
    return week_numenator_denomenator