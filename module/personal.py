from module.file_readers import DataFile

class Personal:
    def __init__(self):
        self.pagename = "Информация о доходах"
        self.items = {}

    def read(self, data_reader: DataFile):
        data_reader.set_current_sheet(self.pagename)
        index = 0
        for record in data_reader:
            if index != 0:
                if not self.items.get(record[2]):
                    self.items[record[2]] = {"company_id": record[1],"id": record[2],'salary':[]}
                self.items[record[2]]['salary'].append( \
                    {
                        "part": record[3],
                        "summa_calculation": record[4],
                        "tax": record[5],
                        "summa": round(float(record[4]) - (float(record[4]) * float(record[5]) / 100), 2) if record[4] and record[5] else 0
                    }
                )
            index += 1

