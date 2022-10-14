from functools import reduce
import os, pathlib, json
from module.file_readers import get_file_reader
from module.company import Company
from module.personal import Personal
from module.polling import Polling
import numpy as np
import matplotlib.pyplot as plt


class Finance:
    def __init__(self, file_name: str):
        self.name = file_name
        self.records = []
        self.company = Company()
        self.personal = Personal()
        self.polling = Polling()
        self.analisys = {}

    def _get_data_xls(self):
        ReaderClass = get_file_reader(self.name)
        data_reader = ReaderClass(self.name)
        if not data_reader:
            raise Exception(f"file reading error: {self.name}")
        return data_reader

    def read(self) -> bool:
        data_reader = self._get_data_xls()
        self.company.read(data_reader)
        self.personal.read(data_reader)
        self.polling.read(data_reader)
        self.analysis()
        self.write(self.company.items, "company")
        self.graph('average','Средняя зарплата')
        self.graph('min','Минимальная зарплата')
        self.graph('max','Максимальная зарплата')

    def analysis(self):
        for id, item in self.company.items.items():
            item["personals"] = list(
                filter(lambda x: x["company_id"] == id, self.personal.items.values())
            )
            item["pollings"] = list(
                filter(lambda x: x["company_id"] == id, self.polling.items.values())
            )

            item["analisys"]["average"] = {
                "real": reduce(self.calc_average, item["personals"], 0)
                / len(item["personals"]),
                "fantastic": reduce(self.calc_average, item["pollings"], 0)
                / len(item["pollings"]),
            }
            item["analisys"]["min"] = {
                "real": reduce(self.calc_min, item["personals"], 0),
                "fantastic": reduce(self.calc_min, item["pollings"], 0),
            }
            item["analisys"]["max"] = {
                "real": reduce(self.calc_max, item["personals"], 0),
                "fantastic": reduce(self.calc_max, item["pollings"], 0),
            }

        return

    def calc_average(self, val_pred: float, elem_curr: dict):
        sum = reduce(lambda x, y: x + y["summa"], elem_curr["salary"], 0) / len(
            elem_curr["salary"]
        )
        return sum + val_pred

    def calc_min(self, value_pred: float, elem_curr: dict):
        value = reduce(
            lambda x, y: y["summa"] if y["summa"] < x or x == 0 else x,
            elem_curr["salary"],
            0,
        )
        return value if value_pred == 0 or value < value_pred else value_pred

    def calc_max(self, value_pred: float, elem_curr: dict):
        value = reduce(
            lambda x, y: y["summa"] if y["summa"] > x or x == 0 else x,
            elem_curr["salary"],
            0,
        )
        return value if value_pred == 0 or value > value_pred else value_pred

    def write(self, item: dict, filename: str):
        os.makedirs("output", exist_ok=True)
        with open(
            pathlib.Path("output", f"{filename}.json"), mode="w", encoding="utf-8"
        ) as file:
            jstr = json.dumps(item, indent=4, ensure_ascii=False)
            file.write(jstr)

    def graph(self, name:str='average', title:str=''):
        #  Задаем смещение равное половине ширины прямоугольника:

        plt.title = title
        x1 = np.arange(1, len(self.company.items) + 1) - 0.2
        x2 = np.arange(1, len(self.company.items) + 1) + 0.2

        y1 = []
        y2 = []
        for item in self.company.items.values():
            y1.append(item["analisys"][name]["real"])
            y2.append(item["analisys"][name]["fantastic"])

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width=0.4)
        ax.bar(x2, y2, width=0.4)

        ax.set_facecolor("seashell")
        fig.set_figwidth(12)  #  ширина Figure
        fig.set_figheight(6)  #  высота Figure
        fig.set_facecolor("floralwhite")

        plt.show()
