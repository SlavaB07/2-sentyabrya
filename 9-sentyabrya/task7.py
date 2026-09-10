class Graph:
    def __init__(self, data):
        self.data = data[:]  
        self.is_show = True
    def show_table(self):
        if not self.is_show:
            print("Отображение данных закрыто")
            return
        print(' '.join(map(str, self.data)))
    def set_show(self, fl_show):
        self.is_show = fl_show
data_graph = [10, 20, 30, 40, 50]
gr = Graph(data_graph)
gr.show_table()
gr.set_show(False)
gr.show_table()