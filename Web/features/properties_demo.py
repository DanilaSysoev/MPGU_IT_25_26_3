class Widget:
    def __init__(self, data):
        self.__data = data

    def get_data(self):
        return self.__data

    def set_data(self, value):
        self.__data = value

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value):
        self.__data = value


def main():
    w1 = Widget(10)
    w2 = Widget("Hello")
    
    print(w1.get_data())
    # w1.set_data(20)
    print(w1.get_data())
    
    print(w2.data)
    w2.data = "world"
    print(w2.data)


if __name__ == "__main__":
    main()