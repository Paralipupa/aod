from module.file_readers import DataFile

class Polling:
    def __init__(self):
        self.pagename = "Результаты опроса о доходах"
        self.items = {}

    def read(self, data_reader: DataFile):
        data_reader.set_current_sheet(self.pagename)
        index = 0
        for record in data_reader:
            if index != 0:
                if not self.items.get(record[1]):
                    self.items[record[1]] = {"company_id": record[5], "company_name": record[1], 'salary':[]}
                self.items[record[1]]['salary'].append( \
                    {
                        "number": record[0],
                        "sex": record[2],
                        "age": record[3],
                        "summa": float(record[4]) if record[4] else 0,
                    }
                )
            index += 1
