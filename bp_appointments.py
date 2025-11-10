from models import Appointments, Pets, Vets, session
from datetime import datetime
from bp_pets import view_pets
from rich import print

#IMPORTANT when creating an appointment, it is required to convert the date string
# "YYYY-MM-DD" int a python date object

date_format = "%Y-%m-%d" #This will be used to format your date

#Syntax for date conversion

# new_date = datetime.strptime("Date String", date_format)
#example
# today = datetime.strptime("2025-08-08", date_format)

def view_vets():
    print("\n[#c65102]----- Show Vets -----")
    vets_list = session.query(Vets).all()
    for vet in vets_list:
        print(f"\n[blue]-------------- Vet Id : {vet.id} ----------------")
        print(f"[blue]Vet Name :[/blue] {vet.name}")
        print(f"[blue]Vet Specialization :[/blue] {vet.specialization}")
        print(f"[blue]Vet Email :[/blue] {vet.email}")

def show_single_appointment(appointment):
    print(f"\n[blue]-------------- Appointment: {appointment.id} ----------------")
    print(f"[blue]Vet:[/blue] {appointment.vet.name}")
    print(f"[blue]Pet:[/blue] {appointment.pet.name}")
    print(f"[blue]Date:[/blue] {appointment.appointment_date}")
    print(f"[blue]Notes :[/blue] {appointment.notes}")
    print(f"[blue]Status :[/blue] {appointment.status}")
    

#Create new appointment
def schedule_appointments(current_user):
    print("\n[#c65102]----- Schedule An Appointment -----")
    try:
        #display pets
        view_pets(current_user)
        #Choose the pet you wish to create an appointment for
        choice = input("Select a pet name: ")
        #query them out of the db using their name
        pet_to_get_appointment = session.query(Pets).where(Pets.name == choice and Pets.owner_id == current_user.id).first()
        #display vets
        view_vets()
        #Choose the vet you with to create an appointment with
        vet_choice = int(input("Select a vet id: "))
        #Query them out of the db
        vet_to_have_appointment = session.query(Vets).where(Vets.id == vet_choice).first()
        #Gather the rest of the info for the appointment
        date = input("Enter the Appointment Date('YYYY-mm-dd'): ")
        #Convert the date string to python date object
        appointment_date = datetime.strptime(date, date_format)
        notes = input("Enter Notes(Optional): ")
        status = input("Enter Status(Optional, default:'Scheduled'): ")
        if not status:
            status = "Scheduled"
            
        #Create the Appointment() (remind you'll need the pet id and the vet id)
        appointment_data = {
            'appointment_date' : appointment_date,
            'notes' : notes,
            'status' : status,
            'pet' : pet_to_get_appointment,
            'vet' : vet_to_have_appointment
        }
        new_appointment = Appointments(**appointment_data)
        session.add(new_appointment)
        session.commit()
        print(f"[green]appointment {new_appointment.id} successfully added.")
        show_single_appointment(new_appointment)
    except Exception as e:
        print("[red]An error occurred while trying to schedule an appointment")
        print(e)  


def view_appointments(current_user, is_not_completed=False):
# By default, show all appointments
    if(is_not_completed):
        print(f"\n[#c65102]-------Show All Uncompleted Appointments: owner name: {current_user.name}------")
    else:
        print(f"\n[#c65102]-------All Appointments: owner name: {current_user.name}------")
    if len(current_user.pets) > 0 :
        for pet in current_user.pets:
            if len(pet.appointments) > 0:
                for appointment in pet.appointments:
                    if(is_not_completed):
                        if(appointment.status != "complete"):
                            show_single_appointment(appointment)
                    else:
                        show_single_appointment(appointment)
            else:
                print(f"\n[yellow]{pet.name} has no appointment.")
    else:
        print(f"\n[yellow]{current_user} has no pet")
        return False
    return True



#Reschedule appointments
def reschedule_appointment(current_user):
    print("\n[#c65102]----- Reschedule An Appointment -----")
    #Show appointments with ids (Loop over current user pets, loop over each pets appointments e.g nested loop)
    is_appointment = view_appointments(current_user,is_not_completed=True)
    if is_appointment:
        try:
            #Select an appointment by id
            choice = int(input("Enter the appointment id: "))
            appointment_to_update = session.query(Appointments).where(Appointments.id == choice).first()
            #ask user for new date
            new_date = input("Enter the Rescheduled Appointment Date('YYYY-mm-dd'): ")
            #convert date
            appointment_new_date = datetime.strptime(new_date, date_format)
            #update the appointment date
            appointment_to_update.appointment_date = appointment_new_date
            session.commit()
            print(f"[green]appointment {appointment_to_update.id} updated successfully.")
        except Exception as e:
            print("[red]An error occurred while trying to reschedule the appointment")
            print(e)  

#Complete appointments
def complete_appointment(current_user):
    print("\n[#c65102]----- Complete An Appointment -----")
    #Show appointments with ids (Loop over current user pets, loop over each pets appointments e.g nested loop)
    is_appointment = view_appointments(current_user,is_not_completed=True)
    if is_appointment:
        try:
            #Select an appointment by id
            choice = int(input("Enter the appointment id: "))
            #query the appointment by id
            appointment_to_complete = session.query(Appointments).where(Appointments.id == choice).first()
            #change appointment.status to 'complete"
            appointment_to_complete.status = "complete"
            session.commit()
            #print success message
            print(f"[green]appointment {appointment_to_complete.id} is successfully completed.")
        except Exception as e:
            print("[red]An error occurred while trying to complete the appointment")
            print(e)  

# Cancel an appointment
def cancel_appointment(current_user):
    print("\n[#c65102]----- Cancel An Appointment -----")
    is_appointment = view_appointments(current_user,is_not_completed=True)
    if is_appointment:
        try:
            #Select an appointment by id
            choice = int(input("Enter the appointment id you want to cancel: "))
            #query the appointment by id
            appointment_to_cancel = session.query(Appointments).where(Appointments.id == choice).first()
            confirm_choice = input("Type 'delete' to confirm you wish to delete your account: ")
            if confirm_choice == "delete":
                session.delete(appointment_to_cancel)
                #commit changes
                session.commit()
                print(f"[green]Successfully appointment {appointment_to_cancel.id} canceled.")
            else:
                print("[red]Invalid choice.")
        except Exception as e:
            print("[red]An error occurred while trying to cancel the appointment")
            print(e)  



