class Dog:
    kind = 'canine'
    def __init__(self, name) -> None:
        self.name = name

d = Dog("Fido")
print(d.name)
print(d.kind)