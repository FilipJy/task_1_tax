from tax_cal import Locality, Estate, Residence
from owner_registry import owner
import json
import os



#načíst města
with open('cities.json', 'r', encoding='utf-8') as file:
    cities = json.load(file)

#volba lokality
def get_locality_info():
    while True:
        name = input("Zadejte název lokality (město): ").strip()
        
        city_info = next((city for city in cities if city['name'].lower() == name.lower()), None)
        
        if city_info:
            coef = city_info['coeficient']
            return Locality(name, coef)
        else:
            print("Město nenalezeno. Zkuste to prosím znovu.")
                

#výpočet daně pro pozemek
def calculate_estate_tax():
    clear_terminal()
    print("\n--- Výpočet daně pro pozemek ---")
    locality = get_locality_info()


    #zvolit typ pozemku
    estate_types = ["zemědělský", "stavební", "les", "zahrada"]
    while True:
        estate_type = input(f"Zadejte typ pozemku ({', '.join(estate_types)}): ").strip().lower()
        if estate_type in estate_types:
            break
        else:
            print("Neplatný typ pozemku. Prosím zkuste znovu.")

    #zadat plochu pozemku
    while True:
        try:
            area = float(input("Zadejte plochu pozemku v m²: ").strip())
            if area <= 0:
                print("Plocha musí být kladné číslo.")
                continue
            break
        except ValueError:
            print("Neplatný vstup. Prosím zadejte číselnou hodnotu.")

    estate = Estate(locality, estate_type, area)
    try:
        tax = estate.calculate_tax()
        clear_terminal()
        print(f"\n{estate}")
        print(f"Vypočtená daň: {tax} Kč")
    except ValueError as e:
        print(f"Chyba při výpočtu daně: {e}")

    save_choice = input("Chcete uložit tento pozemek k majiteli? (ano/ne): ").strip().lower()
    if save_choice == "ano":
        owner_id = input("Zadejte ID majitele: ").strip()
        if os.path.exists("registr.json"):
            with open("registr.json", "r", encoding="utf-8") as file:
                try:
                    owners = json.load(file)
                except json.JSONDecodeError:
                    owners = []
        else:
            owners = []

        for owner in owners:
            if owner["id"] == int(owner_id):
                if "estates" not in owner:
                    owner["estates"] = []
                owner["estates"].append({
                    "locality": locality.name,
                    "type": estate_type,
                    "area": area,
                    "tax": tax
                })
                with open("registr.json", "w", encoding="utf-8") as file:
                    json.dump(owners, file, ensure_ascii=False, indent=2)
                print("Pozemek byl úspěšně uložen k majiteli.")
                return
        print("Majitel s tímto ID neexistuje.")
    else:
        print("Pozemek nebyl uložen.")


def calculate_residence_tax():
    clear_terminal()
    print("\n--- Výpočet daně pro Stavbu ---")
    locality = get_locality_info()
    
    #zadat plochu stavby
    while True:
        try:
            area = float(input("Zadejte plochu stavby v m²: ").strip())
            if area <= 0:
                print("Plocha musí být kladné číslo.")
                continue
            break
        except ValueError:
            print("Neplatný vstup. Prosím zadejte číselnou hodnotu.")

    #zvolit zda je stavba komerční
    while True:
        commercial_input = input("Jedná se o komerční stavbu? (ano/ne): ").strip().lower()
        if commercial_input in ["ano", "ne"]:
            commercial = True if commercial_input == "ano" else False
            break
        else:
            print("Neplatná odpověď. Prosím zadejte 'ano' nebo 'ne'.")

    residence = Residence(locality, area, commercial)
    tax = residence.calculate_tax()
    clear_terminal()
    print(f"\n{residence}")
    print(f"Vypočtená daň: {tax} Kč")

    save_choice = input("Chcete uložit tuto stavbu k majiteli? (ano/ne): ").strip().lower()
    if save_choice == "ano":
        print_owners()
        owner_id = input("Zadejte ID majitele: ").strip()
        if os.path.exists("registr.json"):
            with open("registr.json", "r", encoding="utf-8") as file:
                try:
                    owners = json.load(file)
                except json.JSONDecodeError:
                    owners = []
        else:
            owners = []

        for owner in owners:
            if owner["id"] == int(owner_id):
                if "residences" not in owner:
                    owner["residences"] = []
                owner["residences"].append({
                    "locality": locality.name,
                    "area": area,
                    "tax": tax
                })
                with open("registr.json", "w", encoding="utf-8") as file:
                    json.dump(owners, file, ensure_ascii=False, indent=2)
                print("Stavba byla úspěšně uložena k majiteli.")
                return
        print("Majitel s tímto ID neexistuje.")
    else:
        print("Stavba nebyla uložena.")

def calculate_all_tax():
    clear_terminal()
    print("\n --- Výpočet daně - hromadné ---")

    if os.path.exists("registr.json"):
        with open("registr.json", "r", encoding="utf-8") as file:
            try:
                owners = json.load(file)
            except json.JSONDecodeError:
                owners = []
    else:
        owners = []

    owner_id = int(input("Zadejte ID majitele, u kterého chcete spočítat daně: "))
    owner_data = next((owner for owner in owners if owner["id"] == owner_id), None)
    #sečíst daně zvlášť i dohromady
    if owner_data:
        total_estate_tax = sum(estate["tax"] for estate in owner_data.get("estates", []))
        total_residence_tax = sum(residence["tax"] for residence in owner_data.get("residences", []))
        total_tax = total_estate_tax + total_residence_tax

        clear_terminal()
        print(f"\nCelková daň za pozemky: {total_estate_tax} Kč")
        print(f"Celková daň za stavby: {total_residence_tax} Kč")
        print(f"Celková daň: {total_tax} Kč")
    else:
        print("Majitel s tímto ID nebyl nalezen.")

#volba výpočtu daně
def tax():
    clear_terminal()
    while True:
        choice = input("Jakou daň chcete spočítat? (pozemek, stavba, hromadně nebo 'konec' pro ukončení)\n: ").strip().lower()
        if choice == "pozemek":
            calculate_estate_tax()
        elif choice == "stavba":
            calculate_residence_tax()
        elif choice == "hromadně":
            calculate_all_tax()
        elif choice == "konec":
            print("Děkujeme za použití aplikace. Nashledanou!")
            break
        else:
            print("Neplatná volba. Prosím zadejte 'pozemek', 'stavba' nebo 'konec'.")


def new_owner():
    clear_terminal()
    print("\n--- Zápis nového majitele ---")

    #základní info
    name = input("Zadejte jméno majitele: ").strip()
    surname = input("Zadejte příjmení majitele: ").strip()
    birth_date = input("Zadejte datum narození majitele (ve formátu DD.MM.RRRR): ").strip()
    email = input("Zadejte email majitele: ").strip()
    phone_number = input("Zadejte telefonní číslo majitele: ").strip()

    new_owner = owner(name, surname, birth_date, email, phone_number,)
    print(f"Nový majitel: {new_owner}")

    #uložení
    save_choice = input("Chcete uložit nového majitele? (ano/ne): ").strip().lower()
    if save_choice == "ano":
        if os.path.exists("registr.json"):
            #kontrola prázdného jsonu
            if os.path.getsize("registr.json") > 0:
                with open("registr.json", "r", encoding="utf-8") as file:
                    try:
                        owners = json.load(file)
                    except json.JSONDecodeError:
                        owners = []
            else:
                owners = []
        else:
            owners = []

        #kontrola duplicity
        for existing_owner in owners:
            if (existing_owner["name"] == name and
                existing_owner["surname"] == surname and
                existing_owner["birth_date"] == birth_date):
                print("Majitel již existuje.")
                return
            
        #generovat ID    
        if owners:
            max_id = max(owner.get("id", 0) for owner in owners)
            unique_id = max_id + 1
        else:
            unique_id = 1

        new_owner_data = {
            "id": unique_id,
            "name": name,
            "surname": surname,
            "birth_date": birth_date,
            "email": email,
            "phone_number": phone_number
        }

        owners.append(new_owner_data)

        with open("registr.json", "w", encoding="utf-8") as file:
            json.dump(owners, file, ensure_ascii=False, indent=2)

        clear_terminal()
        print(f"Majitel byl úspěšně uložen a bylo mu přideleno ID: {unique_id}.")
    else:
        print("Majitel nebyl uložen.")


def print_owners():
    clear_terminal()
    print("\n--- Výpis majitelů ---")

    if os.path.exists("registr.json"):
        #kontrola prázdného jsonu
        if os.path.getsize("registr.json") > 0:
            with open("registr.json", "r", encoding="utf-8") as file:
                try:
                    owners = json.load(file)
                except json.JSONDecodeError:
                    owners = []
        else:
            owners = []
    else:
        owners = []

    choice = input("Chcete vypsat všechny majitele? (ano/ne): ").strip().lower()
    if choice == "ano":
        clear_terminal()
        #výpis majitelů (všech)
        if owners:
            for owner_data in owners:
                owner_instance = owner(owner_data["name"], owner_data["surname"], owner_data["birth_date"], owner_data["email"], owner_data["phone_number"])
                print(f"\nID: {owner_data['id']}")
                print(owner_instance, "\n")
        else:
            print("V registru nejsou žádní majitelé.")
    else: 
        owner_id = int(input("Zadejte ID majitele, kterého chcete vypsat: "))
        owner_data = next((owner for owner in owners if owner["id"] == owner_id), None)
        if owner_data:
            owner_instance = owner(owner_data["name"], owner_data["surname"], owner_data["birth_date"], owner_data["email"], owner_data["phone_number"])
            clear_terminal()
            print(owner_instance, "\n")
            #výpis majetku, pokud je
            if "estates" in owner_data:
                print("\nPozemky:")
                for estate in owner_data["estates"]:
                    print(f"  Lokalita: {estate['locality']}, Typ: {estate['type']}, Plocha: {estate['area']} m², Daň: {estate['tax']} Kč\n")
            if "residences" in owner_data:
                print("\nStavby:")
                for residence in owner_data["residences"]:
                    print(f"  Lokalita: {residence['locality']}, Plocha: {residence['area']} m², Daň: {residence['tax']} Kč\n")      
        else:
            print("Majitel s tímto ID nebyl nalezen.")



def edit_owner():
    print("\n--- Úprava majitele ---")
    if os.path.exists("registr.json"):
        #kontrola prázdného jsonu
        if os.path.getsize("registr.json") > 0:
            with open("registr.json", "r", encoding="utf-8") as file:
                try:
                    owners = json.load(file)
                except json.JSONDecodeError:
                    owners = []
        else:
            owners = []
    else:
        owners = []

    if owners:
        #výpis majitelů (možná není potřeba)
        print_owners()
        owner_id = int(input("\nZadejte ID majitele, kterého chcete upravit: "))
        owner_data = next((owner for owner in owners if owner["id"] == owner_id), None)
        if owner_data:
            clear_terminal()
            print("\nSoučasné informace o majiteli:")
            owner_instance = owner(owner_data["name"], owner_data["surname"], owner_data["birth_date"], owner_data["email"], owner_data["phone_number"])
            print(owner_instance)

            name = input("Zadejte nové jméno majitele (nechte prázdné pro ponechání původní hodnoty): ").strip()
            surname = input("Zadejte nové příjmení majitele (nechte prázdné pro ponechání původní hodnoty): ").strip()
            birth_date = input("Zadejte nové datum narození majitele (ve formátu DD.MM.RRRR, nechte prázdné pro ponechání původní hodnoty): ").strip()
            email = input("Zadejte nový email majitele (nechte prázdné pro ponechání původní hodnoty): ").strip()
            phone_number = input("Zadejte nové telefonní číslo majitele (nechte prázdné pro ponechání původní hodnoty): ").strip()

            if name:
                owner_data["name"] = name
            if surname:
                owner_data["surname"] = surname
            if birth_date:
                owner_data["birth_date"] = birth_date
            if email:
                owner_data["email"] = email
            if phone_number:
                owner_data["phone_number"] = phone_number

            with open("registr.json", "w", encoding="utf-8") as file:
                json.dump(owners, file, ensure_ascii=False, indent=2)
        
            print("Majitel byl úspěšně upraven.")
        else:
            print("Majitel s tímto ID nebyl nalezen.")

def delete_owner():
    clear_terminal()
    print("\n--- Smazání majitele ---")
    if os.path.exists("registr.json"):
        #kontrola prázdného jsonu
        if os.path.getsize("registr.json") > 0:
            with open("registr.json", "r", encoding="utf-8") as file:
                try:
                    owners = json.load(file)
                except json.JSONDecodeError:
                    owners = []
        else:
            owners = []
    else:
        owners = []

    if owners:
        #výpis majitelů (možná není potřeba)
        print_owners()
        owner_id = int(input("\nZadejte ID majitele, kterého chcete smazat: "))
        owner_data = next((owner for owner in owners if owner["id"] == owner_id), None)
        if owner_data:
            print("\nInformace o majiteli:")
            owner_instance = owner(owner_data["name"], owner_data["surname"], owner_data["birth_date"], owner_data["email"], owner_data["phone_number"])
            print(owner_instance)

            choice = input("Opravdu chcete smazat tohoto majitele? (ano/ne): ").strip().lower()
            if choice == "ano":
                owners.remove(owner_data)
                with open("registr.json", "w", encoding="utf-8") as file:
                    json.dump(owners, file, ensure_ascii=False, indent=2)
                clear_terminal()
                print("Majitel byl úspěšně smazán.")
            else:
                print("Majitel nebyl smazán.")
        else:
            print("Majitel s tímto ID nebyl nalezen.")


def open_registry():
    clear_terminal()
    print("\n--- Vítejte v registru majetku ---")
    while True:
        choice = input("Co chcete udělat? \n(Napiště 'nový' pro zápis nového majitele, 'výpis' pro výpis všech majitelů a majetku, 'úprava' pro úpravu záznamu, 'smazat' pro smazání záznamu nebo 'konec' pro ukončení)\n: ").strip().lower()
        if choice == "nový":
            new_owner()
        elif choice == "výpis":
            print_owners()
        elif choice == "úprava":
            edit_owner()
        elif choice == "smazat":
            delete_owner()
        elif choice == "konec":
            print("Děkujeme za použití aplikace. Nashledanou!")
            break

def clear_terminal():
    os.system("clear")

def main():
    clear_terminal()
    print("Vítejte v aplikaci na výpočet daně.")
    while True:
        choice = input("Co chcete udělat? \n(Napiště 'tax' pro výpočet daně, 'registr' pro zápis nového majitele nebo výpis či úpravu již existujícího záznamu, nebo 'konec' pro ukončení)\n: ").strip().lower()
        if choice == "tax":
            tax()
        elif choice == "registr":
            open_registry()
        elif choice == "konec":
            print("Děkujeme za použití aplikace. Nashledanou!")
            break
        else:
            print("Neplatná volba. Prosím zadejte 'tax', 'registr' nebo 'konec'.")

if __name__ == "__main__":
    main()