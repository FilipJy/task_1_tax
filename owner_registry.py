#majitel
class owner:
    def __init__(self, name, surname, birth_date, email, phone_number):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return f"Jméno: {self.name}, Příjmení: {self.surname}, Datum narození: {self.birth_date}, Email: {self.email}, Telefonní číslo: {self.phone_number}"


#testovací majitel
owner_1 = owner("Lukáš", "Rudý", "20. 5. 1980", "lukas.rudy@gmail.com", "123456789")

print(owner_1)