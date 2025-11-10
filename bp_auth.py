from models import Owners, session #Need the Users model to create and search for users
#need the sesssion to add users to our db
from rich import print



#Create Login function
def login():
    #get email and password from user
    print("\n[#c65102]----- Login to pet clinic -----")
    email = input("Email: ")
    password = input("Password: ")
    user_credentials = {
        'email' : email,
        'password': password
    }
    #check database for owner with the given email
    try:
        user = session.query(Owners).where(Owners.email==user_credentials['email']).first()
        #if you find an owner, check if the found owners password is the same as the given password
        if user and user.password == user_credentials['password']:
            print(f"[green]Successfully logged in {user.name}")
            #if so return user
            return user
        else:
            print("[red]Invalid email or password")
    except Exception as e:
        print("[red]An error occurred while trying to logged in")
        print(e)
        return None


#Create Register function
def register_owner():
    print("\n[#c65102]----- Register to pet clinic -----")
#get all info required to create an owner from the user
    name = input("Enter Your Name: ")
    phone = input("Enter Your Phone: ")
    email = input("Enter Your Email: ")
    password = input("Enter Your Password: ")
    #try and create an Owner from the info (will fail if email is already in user)
    owner_data = {
        'name' : name,
        'phone' : phone,
        'email' : email,
        'password' : password
    }
    try:
        new_user = Owners(**owner_data)
        #if you succeed return user
        session.add(new_user)
        session.commit()
        print(f"[green]{new_user.name} successfully registered, welcome to pet clinic.")
        return new_user
    #except error and print message
    except Exception as e:
        print("[red]An error occurred while trying to create the user")
        print(e)
        return None        


