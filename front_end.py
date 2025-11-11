#DONT FORGET TO IMPORT FUNCTIONS AFTER YOU MAKE THEM
from bp_auth import register_owner, login
from bp_owner import view_profile, update_profile, delete_user
from bp_pets import view_pets, create_pet, update_pet, delete_pet
from bp_appointments import schedule_appointments, view_appointments, reschedule_appointment, complete_appointment,cancel_appointment
from rich import print

def welcome_menu():
    current_user = None
    while True:
        print("""
[purple]--------- Welcome to Pet Clinic --------
    1.)[/purple] Login
    [purple]2.)[/purple] Register
""")
        choice = input("select (1 or 2) or quit: ")
        if choice == '1':
            #login function
            user = login()
            if user:
                #should set the current user on successful login
                return user

        elif choice == '2':
            #register function
            new_owner = register_owner()
            #should set the current user on successful register
            if new_owner:
                return new_owner
            
        elif choice == 'quit':
            return
        
        else:
            print("[red]Invalid response please try again.")

def owner_menu(current_user):
    while True:
        print("""
[purple]--------- Profile Menu --------
    1.)[/purple] View Profile
    [purple]2.)[/purple] Update Profile
    [purple]3.)[/purple] Delete Profile
    [purple]4.)[/purple] Back""")
        choice = input("choose 1-4: ")
        if choice == '1':
            #view profile function should display the current users info
            view_profile(current_user)
        elif choice == '2':
            #update profile function, and returns the updated user
            current_user = update_profile(current_user)
        elif choice == '3':
            #delete the current users account
            is_deleted = delete_user(current_user)
            if is_deleted:
                current_user = None
                main() # Recursively calling my main function to restart the program from the beginning
        elif choice == '4':
            return #Goes back to main menu
        else:
            print("[red]Invalid Selection.")

def pets_menu(current_user):
    while True:
        print("""
[purple]--------- Pet Menu --------
    1.)[/purple] View my Pets
    [purple]2.)[/purple] Create Pet
    [purple]3.)[/purple] Update Pet
    [purple]4.)[/purple] Delete Pet
    [purple]5.)[/purple] Back""")
        choice = input("choose 1-5: ")
        if choice == '1':
            #function that displays the current user's pets
            view_pets(current_user)
        elif choice == '2':
            #function to create a new pet linked to the current user, add to db
            create_pet(current_user)
        elif choice == '3':
            #function to update a particular pet 
            update_pet(current_user)
        elif choice == '4':
            #function to delete a particular pet
            delete_pet(current_user)
        elif choice == '5':
            return
        else:
            print("[red]Invalid Selection.")

def appointments_menu(current_user):
    while True:
        print("""
[purple]--------- Appointment Menu --------
    1.)[/purple] schedule appointment
    [purple]2.)[/purple] view appointments
    [purple]3.)[/purple] reschedule appointment
    [purple]4.)[/purple] Complete appointment
    [purple]5.)[/purple] Cancel appointment
    [purple]6.)[/purple] Back
""")
        choice = input("choose 1-6: ")
        if choice == '1':
            #Function to create a new appointment between one of the user's pets
            #and one of the vets
            schedule_appointments(current_user)
        elif choice == '2':
            #View current user's appointments
            view_appointments(current_user)
        elif choice == '3':
            #Reschedule appointment (change the date)
            reschedule_appointment(current_user)
        elif choice == '4':
            #Complete appointment (change status to complete)
            complete_appointment(current_user)
        elif choice =='5':
            cancel_appointment(current_user)
        elif choice == '6':
            return
        else:
            print("[red]Invalid Selection.")


def main():
    
    current_user = welcome_menu() 

    #After you test you login and register functions, it might be more efficient
    #to set current_user to a user in your db so you don't have to log in every time
    #you want to test something.
    
    if current_user:
        while True:
            print("""
[purple]--------- Pet Clinic --------
    1.)[/purple] Manage Profile
    [purple]2.)[/purple] My Pets
    [purple]3.)[/purple] My Appointments
    [purple]4.)[/purple] Log out
""")
            choice = input("choose 1-4: ")
            if choice == '1':
                owner_menu(current_user)
            elif choice == '2':
                pets_menu(current_user)
            elif choice == '3':
                appointments_menu(current_user)
            elif choice == '4':
                current_user = None
                main()
            else:
                print("[red]Invalid Selection.")
    

main()
    
