class EmailUtil:

    @staticmethod
    def send(data):
        print("subject={}\nfrom={}\nto={}\ncontent={}\n".format(data[0], data[1], data[2], data[3]))
