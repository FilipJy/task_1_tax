import math

#lokalita
class Locality:
    def __init__(self, name, locality_coeficient):
        self.name = name
        self.locality_coeficient = locality_coeficient
    def __str__(self):
        return f"{self.name}, Koeficient lokality: {self.locality_coeficient}"
    

#nemovistost
class Property:
    def __init__(self, locality):
        self.locality = locality
    
    def __str__(self):
        return f"lokalita: {self.locality}"


#pozemek
class Estate(Property):
    def __init__(self, locality, estate_type, area):
        super().__init__(locality)
        self._estate_type = estate_type.lower()
        self.area = area

    coefficients = {
        "zemědělský": 0.85,
        "stavební": 9,
        "les": 0.35,
        "zahrada": 2
    }
    
    @property
    def estate_type(self):
        return self.coefficients.get(self._estate_type, "Unknown")
    
    def calculate_tax(self):    
        return math.ceil(self.area * self.estate_type * self.locality.locality_coeficient)


    def __str__(self):
        return f"Lokalita: {self.locality}, Typ pozemku: {self._estate_type}, Koeficient typu pozemku: {self.estate_type}, Plocha: {self.area}m2"


#stavba
class Residence(Property):
    def __init__(self, locality, area, commercial):
        super().__init__(locality)
        self.area = area
        self.commercial = commercial

    def calculate_tax(self):
        if self.commercial == True:
             return math.ceil(self.area * self.locality.locality_coeficient * 15 * 2)
        else:
             return math.ceil(self.area * self.locality.locality_coeficient * 15)
        
    def __str__(self):
        return f"Lokalita: {self.locality}, Plocha: {self.area}m2, Komercni: {self.commercial}"
       

#testovací
Brno = Locality("Brno", 1.2)
Praha = Locality("Praha", 1.5)
pozemek_1 = Estate(Brno, "zemědělský", 500)
stavba_1 = Residence(Brno, 57, True)
stavba_2 = Residence(Praha, 35, False)

print(stavba_1)
print(stavba_1.calculate_tax())



