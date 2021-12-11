import pickle


class PersistUploader:
    def __init__(self, picklefile="persist_picklefile"):
        self.filename = picklefile

    def add_new_item(self, item):
        with open(self.filename, "ab") as fp:
            pickle.dump(item, fp)

    def load_items(self):
        data = []
        with open(self.filename, 'rb') as fr:
            try:
                while True:
                    data.append(pickle.load(fr))
            except EOFError:
                pass

        return data
