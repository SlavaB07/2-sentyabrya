import sys

class StreamData:
    def create(self, fields, lst_values):
        if len(fields) != len(lst_values):
            return False
        for i, field in enumerate(fields):
            setattr(self, field, lst_values[i])
        return True

class StreamReader:
    FIELDS = ('id', 'title', 'pages')

    def readlines(self):
        lst_in = list(map(str.strip, sys.stdin.readlines()))
        sd = StreamData()
        res = sd.create(self.FIELDS, lst_in)
        return sd, res

if __name__ == "__main__":

    sr = StreamReader()
    data, result = sr.readlines()
    print(f"Результат: {result}")
    if result:
        print(f"id: {data.id}")
        print(f"title: {data.title}")
        print(f"pages: {data.pages}")