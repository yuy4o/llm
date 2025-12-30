class human:
    def __init__(self, name, age, favorite_color):
        self.name = name
        self.age = age
        self.favorite_color = favorite_color

    # You can use the __str__() function to define what is returned when the object is represented as a string.
    def __str__(self):
        info_str = f"{self.name} is {self.age} years old and their favorite color is {self.favorite_color}."
        return info_str


new_human = human("John", 42, "Blue")

print(new_human)

# You can modify object properties:
new_human.age = 52
print(new_human)

# You can also delete object properties:
del new_human.age
print(new_human)  # This will now produce an error

# You can also delete objects:
del new_human
print(new_human)  # This will now produce a different error
