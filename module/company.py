from module.file_readers import DataFile

class Company:
    def __init__(self):
        self.pagename = "Справочник компаний"
        self.items = {}

    def read(self, data_reader: DataFile):
        data_reader.set_current_sheet(self.pagename)
        index = 0
        for record in data_reader:
            if index != 0:
                self.items[record[0]] = \
                    {
                        "id": record[0],
                        "name": record[1],
                        "count": record[2],
                        "type": record[3],
                        "personals": [],
                        "pollings": [],
                        "analisys": {}
                    }
            index += 1
