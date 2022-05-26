import datetime
import time
import threading
from whatsappbot.services.regex_validation import GET_DATA_NA, GET_SEPARATOR

WAIT_8_HOURS = 28800
dias_semana_l = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
dias_semana_d = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo"
}
dias_semana_por_data = {

}


def getDayFormatted(day, hour=9):
    d_inicial = datetime.datetime(year=datetime.datetime.now().year,
                                  month=datetime.datetime.now().month,
                                  day=day,
                                  hour=hour, minute=0, second=0, microsecond=000)
    d_inicial = datetime.datetime.isoformat(d_inicial)
    d_inicial += "-03:00"
    return d_inicial


def create_days_week():
    data = datetime.datetime.now()
    today = data.day
    today_week = data.weekday()
    data_semana = "{}-{:02d}-{}".format("{:02d}", data.month, data.year)
    global dias_semana_por_data
    for d in range(1, 7):
        today_week = (today_week + 1) % 7
        dia = today + d
        if dia >= 31:
            dia = dia % 31
            dia += 1
        dias_semana_por_data[dia] = (dias_semana_d[today_week], data_semana.format(today + d))


def get_dayname_from_day(day):
    return dias_semana_por_data[day][0]


def get_day_from_dayname(dayname):
    for d in dias_semana_por_data:
        if dayname in dias_semana_por_data[d][0]:
            return d
    return -1


def get_dayname_from_data(data):
    for d in dias_semana_por_data:
        if data in dias_semana_por_data[d][1]:
            return dias_semana_por_data[d][0]
    return "não encontrado"


def get_data_from_day(day):
    return dias_semana_por_data[day][1]


def get_data_from_dayname(dayname):
    for d in dias_semana_por_data:
        if dayname in dias_semana_por_data[d][0]:
            return dias_semana_por_data[d][1]
    return -1


def get_day_from_data(data):
    for d in dias_semana_por_data:
        if data in dias_semana_por_data[d][1]:
            return d
    return -1


# def ajuste_dias_semana_por_data():
#     while True:
#         create_days_week()
#         time.sleep(WAIT_8_HOURS)

def get_days_options_format():
    create_days_week()
    days = ""
    for i, d in enumerate(dias_semana_por_data.keys()):
        days += f"{dias_semana_por_data[d][0].title()} ({dias_semana_por_data[d][1]})\n"
    return days

def convert_data_to_dd_mm_yyyy(data):
    data_formated = GET_DATA_NA.search(data).group()
    separator = GET_SEPARATOR.search(data).group()
    data_formated = data_formated.split(separator)
    data_formated = f"{data_formated[2]}{separator}{data_formated[1]}{separator}{data_formated[0]}"
    return data_formated

create_days_week()
# def start_thread():
#     t = threading.Thread(target=ajuste_dias_semana_por_data, args=())
#     t.start()