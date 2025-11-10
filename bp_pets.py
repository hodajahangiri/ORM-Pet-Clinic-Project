from models import Pets, Appointments, session
from rich import print

#view pets function
def view_pets(current_user):
    print("\n[#c65102]----- View Pets -----")
    #Takes in current user
    #Loops over all of the current users pets (use the .pets relationship attribute to get list of pets)
    if len(current_user.pets) > 0:
        for pet in current_user.pets:
        #prints the pets info
            show_single_pet(pet)
    else:
        print(f"[yellow]{current_user.name} doesn't have a pat.")


def show_single_pet(pet):
    print(f"\n[blue]-------------- Pet: {pet.id} ----------------")
    print(f"[blue]Name:[/blue] {pet.name}")
    print(f"[blue]Species:[/blue] {pet.species}")
    print(f"[blue]Breed :[/blue] {pet.breed}")
    print(f"[blue]Age :[/blue] {pet.age}")

#Create pets function
def create_pet(current_user):
    print("\n[#c65102]----- Add a Pet -----")
    #gets pets info from user
    try:
        name = input("Enter Pet Name: ")
        species = input("Enter Pet Species: ")
        breed = input("Enter Pet Breed: ")
        age = int(input("Enter Pet Age: "))
        pet_data = {
            'name' : name,
            'species' : species,
            'breed' : breed,
            'age' : age,
            'owner': current_user
        }
        #create Pets() from the info
        new_pet = Pets(**pet_data)
        session.add(new_pet)
        session.commit()
        print(f"[green]{new_pet.name} successfully added as {current_user.name}  pet.")
        #print new pet
        show_single_pet(new_pet)
    #except error and print message
    except Exception as e:
        print("[red]An error occurred while trying to create the user")
        print(e)
        return None        




#Update pets function
def update_pet(current_user):
    print("\n[#c65102]----- Update Pet Information -----")
    #display current users pets
    view_pets(current_user)
    if len(current_user.pets) > 0:
        #allow them to select a pet BY Name
        choice = input("Select a pet name: ")
        #query that pet from the database
        pet_to_update = session.query(Pets).where(Pets.name == choice and Pets.owner_id == current_user.id).first()
        #get updated info from the user
        if pet_to_update:
            show_single_pet(pet_to_update)
            #set that pets info to the new info
            print("[yellow]Make your changes, leave blank if you want to keep current value")
            name = input("Enter Pet Name: ")
            species = input("Enter Pet Species: ")
            breed = input("Enter Pet Breed: ")
            age = input("Enter Pet Age: ")
            if name:
                pet_to_update.name = name
            if species:
                pet_to_update.species = species
            if breed:
                pet_to_update.breed = breed
            if age:
                pet_to_update.age = int(age)
            #commit changes
            session.commit()
            #print new pet info
            show_single_pet(pet_to_update)
        else:
            print("[red]Invalid choice")


#Delete pets function
def delete_pet(current_user):
    print("\n[#c65102]----- Delete a Pet -----")
    try:
        #display current users pets
        view_pets(current_user)
        if len(current_user.pets) > 0:
            #allow them to select a pet BY NAME
            choice = input("Select a pet name: ")
            #query that pet from the database
            pet_to_delete = session.query(Pets).where(Pets.name == choice and Pets.owner_id == current_user.id).first()
            show_single_pet(pet_to_delete)
            #Ask user if they are sure they want to delete this pet
            confirm_choice = input("Type 'delete' to confirm you wish to delete your account: ")
            if confirm_choice == "delete":
                if len(pet_to_delete.appointments) > 0:
                    session.query(Appointments).where(Appointments.pet_id == pet_to_delete.id).delete(synchronize_session=False)
                    session.commit()
                #delete pet from the session
                session.delete(pet_to_delete)
                #commit changes
                session.commit()
                print(f"[green]Successfully deleted pet: {choice}")
            else:
                print("[red]Invalid choice.")
    except Exception as e:
        print("[red]An error occurred while trying to delete the pet")
        print(e)  
    






