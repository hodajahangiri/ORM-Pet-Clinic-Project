from models import session, Appointments, Pets
from rich import print

#View profile function
def view_profile(current_user):
    print("\n[#c65102]----- View Profile -----")
    #displays the current users info
    print(f"[blue]--- {current_user.name} ---")
    print(f"[blue]Email:[/blue] {current_user.email}")
    print(f"[blue]password:[/blue] {current_user.password}")
    print(f"[blue]phone:[/blue] {current_user.phone}")


#Update profile function
def update_profile(current_user):
    print("\n[#c65102]----- Update Profile -----")
    #displays current user info
    view_profile(current_user)
    print("[yellow]Make your changes, leave blank if you want to keep current value")
    #allows user to update any of the fields
    name = input("Enter Your Name: ")
    phone = input("Enter Your Phone: ")
    email = input("Enter Your Email: ")
    password = input("Enter Your Password: ")
    #commits changes
    if name:
        current_user.name = name
    if phone:
        current_user.phone = phone
    if email:
        current_user.email = email
    if password:
        current_user.password = password
    session.commit()
    print("[green]Here are your new changes: ")
    #shows changes and returns update current_user
    view_profile(current_user)
    return current_user

#Delete user function
def delete_user(current_user):
    print("\n[#c65102]----- Delete User -----")
    #Ask user to confirm they want to delete
    choice = input("Type 'delete' to confirm you wish to delete your account: ")
    #if so delete the current user from the session
    if choice == "delete":
        # We need to delete all pets and appointments for thi owner. 
        if len(current_user.pets) > 0 :
            for pet in current_user.pets:
                if len(pet.appointments) > 0:
                    session.query(Appointments).where(Appointments.pet_id == pet.id).delete(synchronize_session=False)
                    session.commit()
            session.query(Pets).where(Pets.owner_id == current_user.id).delete(synchronize_session=False)
            session.commit()
        session.delete(current_user)
        #commits changes 
        session.commit()
        print("[green]Successfully deleted account")
        return True
    else:
        return False
                