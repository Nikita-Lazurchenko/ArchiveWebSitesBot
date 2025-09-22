import datetime
import re

import requests

def get_date_saves_url(site):
    url = "https://web.archive.org/cdx/search/cdx?url=%s" % site
    response = requests.get(url)
    answer = response.text
    data_saves_array = re.findall(r'\d{14}', answer)

    return data_saves_array


def get_dates_matrix_by_year(site):
    data_saves_array = get_date_saves_url(site)
    data = data_saves_array[0][:4]

    dates_matrix = []
    data_array = ["Сохранения за {} год: \n".format(data)]
    for data_save in data_saves_array:
        if data in data_save:
            data_parse_to_datetime = datetime.datetime.strptime(data_save, "%Y%m%d%H%M%S")
            data_array.append("Сохранение на момент %s : http://web.archive.org/web/%s/%s/\n" % (data_parse_to_datetime,data, site))
            if len(data_array) == 10:
                dates_matrix.append(data_array)
                data_array = []
        else:
            data = data_save[:4]
            if len(data_array)!=0:
                dates_matrix.append(data_array)
            data_array = ["Сохранения за {} год: \n".format(data)]

    if data_array:
        dates_matrix.append(data_array)

    return dates_matrix

def get_file_available_snapshots(site):
    data_saves_array = get_date_saves_url(site)
    data = data_saves_array[0][:4]

    dir = f"C:\\Users\\admin\\ArchiveWebSitesBot\\{site}.txt"
    file = open(dir, 'wt')
    snapshots_in_one_year = "Сохранения за {} год: \n".format(data)
    for data_save in data_saves_array:
        if data in data_save:
            data_parse_to_datetime = datetime.datetime.strptime(data_save, "%Y%m%d%H%M%S")
            snapshots_in_one_year += "Сохранение на момент %s : http://web.archive.org/web/%s/%s/\n" % (data_parse_to_datetime, data, site)
        else:
            data = data_save[:4]
            file.write(snapshots_in_one_year)
            snapshots_in_one_year = "Сохранения за {} год: \n".format(data)

    if  snapshots_in_one_year :
        file.write(snapshots_in_one_year)

    file.close()
    return dir

text = get_file_available_snapshots("donnu.ru")
print(text)