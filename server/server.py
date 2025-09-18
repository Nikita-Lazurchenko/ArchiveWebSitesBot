import datetime
import re

import requests

def get_list_available_snapshots(site):
    url = "https://web.archive.org/cdx/search/cdx?url=%s" % site
    response = requests.get(url)
    answer = response.text
    data_saves_array = re.findall(r'\d{14}', answer)
    data_saves_matrix = get_dates_matrix_by_year(data_saves_array,site)

    return data_saves_matrix


def get_dates_matrix_by_year(data_saves_array,site):
    data = data_saves_array[0][:4]

    dates_matrix = []
    data_array = ["Сохранения за {} год: \n".format(data)]
    for data_save in data_saves_array:
        if data in data_save:
            data_parse_to_datetime = datetime.datetime.strptime(data_save, "%Y%m%d%H%M%S")
            data_array.append("Сохранение на момент %s : http://web.archive.org/web/%s/%s/\n" % (data_parse_to_datetime,data, site))
        else:
            data = data_save[:4]
            dates_matrix.append(data_array)
            data_array = ["Сохранения за {} год: \n".format(data)]

    if data_array:
        dates_matrix.append(data_array)

    return dates_matrix