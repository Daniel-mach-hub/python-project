import json
from datetime import date
from data.storage import load_data, save_data

def show_menu():
    print("\nPet Adoption CLI")
    print("1. View all adoptable pets")
    print("2. Register a new adopter")
    print("3. Adopt a pet")
    print("4. View adoption history")
    print("5. Exit")

def view_pets(data):
    print("\nAvailable Pets:")
    for pet in data["pets"]:
        if not pet["adopted"]:
            print(f"{pet['id']}: {pet['name']} ({pet['species']}, {pet['age']} yrs)")

def register_adopter(data):
    adopter = {
        "id": len(data["adopters"]) + 1,
        "name": input("Name: "),
        "phone": input("Phone: "),
        "email": input("Email: ")
    }
    data["adopters"].append(adopter)
    print("Adopter registered.")

def adopt_pet(data):
    adopter_id = int(input("Adopter ID: "))
    pet_id = int(input("Pet ID: "))
    pet = next((p for p in data["pets"] if p["id"] == pet_id and not p["adopted"]), None)
    if pet:
        pet["adopted"] = True
        adoption = {
            "adopter_id": adopter_id,
            "pet_id": pet_id,
            "adoption_date": str(date.today())
        }
        data["adoptions"].append(adoption)
        print("Pet adopted!")
    else:
        print("Pet not found or already adopted.")

def view_adoptions(data):
    print("\nAdoption History:")
    for record in data["adoptions"]:
        adopter = next(a for a in data["adopters"] if a["id"] == record["adopter_id"])
        pet = next(p for p in data["pets"] if p["id"] == record["pet_id"])
        print(f"{adopter['name']} adopted {pet['name']} on {record['adoption_date']}")

def main():
    data = load_data()
    while True:
        show_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            view_pets(data)
        elif choice == "2":
            register_adopter(data)
        elif choice == "3":
            adopt_pet(data)
        elif choice == "4":
            view_adoptions(data)
        elif choice == "5":
            save_data(data)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
