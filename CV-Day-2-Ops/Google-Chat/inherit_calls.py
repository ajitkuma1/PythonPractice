class books:
    def __init__(self, title, author, quantity, price ):
        self.title = title 
        self.author = author 
        self.quantity = quantity 
        self.price = price 
        self.__discount = None
    
    def set_discount(self, discount):
        self.__discount = discount 
    
    def get_price(self) -> int:
        if self.__discount: 
            #print (f"Price of the book is {self.price * self.__discount}")
            return self.price * (1-self.__discount)
        #print (f"Price of the book is {self.price}")
        return  self.price * self.__discount
    
    def __repr__(self):
        return f"Title: {self.title}, Author: {self.author} Quantity: {self.quantity} Price: {self.get_price()}"
    

class Novel(books):
    def __init__(self, title, author, quantity, price, pages):
        super().__init__(title, author, quantity, price)
        self.pages = pages

class acadamic(books):
    def __init__(self, title, author, quantity, price, branch):
        super().__init__(title, author, quantity, price)
        self.branch = branch


N = Novel ("Mindset", "Doyle", 10, 135, 239)
N.set_discount(0.10)
#print(N.get_price)
#print(N.get_price)
print(N)