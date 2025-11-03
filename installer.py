#Initialize project and provide a installer for local enviroments in new systems. 
import os,sys,asyncio
import subprocess as sb

def main():
    while True:
        try:
            ans = greet_user()
            ans = parse_yesno(ans)
            if ans = "yes":
                start_Install()
            else:
                print("Goodbye")
                sys.exit()
        Except Exception as e:
            print(e)

def greet_user():
    print(f"Welcome to LRAT!\n")
    print("This script will access your local enviroment to install the LRAT\n
          program and it's dependancies. Do you wish to continue?")
    user_answer = input("Y/N")
    return user_answer

def parse_yesno(x):
    match x:
        case "y":
            return "yes"
        case "Y":
            return "yes"
        case "n":
            return "no"
        case "N":
            return "no"
        case "yes":
            return "yes"
        case "YES":
            return "yes"
        case "No":
            return "no"
        case "NO":
            return "no"
        case _:
            print("Please select a valid option")



def start_Install():
    async 


asyncio.run(main())


