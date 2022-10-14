class Person:
    def __init__(self, name, age, location):
        self.name = name
        self.age = age 
        self.location = location 
        self.__hobby = None
    
    def __repr__(self):
        return f"Name: {self.name}, Age: {self.age}, Location: {self.location}"
    
    def set_hobby(self, hobby: str):
        self.__hobby = hobby

    def get_hobby(self):
        if self.__hobby:
            return f"{self.name} is a {self.__hobby} player"
        else:
            return f"{self.name} is a {self.__hobby} player - Not a cricket player :("
            print(f"{self.name} is a {self.__hobby} player - Not a cricket player :(")
    

T = Person("Ajitesh", 40, "Bangalore")
T.set_hobby(1)
print(T.get_hobby())

S = Person("Swati", 16, "Bangalore")
S.set_hobby("Volleyball")
print(S.get_hobby())

print(T)
print(S)

#print("Name: {}".format(T.name))

#print(f"Name: {T.name}")
#print(f"Hobby: {T.__hobby}")