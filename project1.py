""" project 1"""
import numpy as np

def login():
    while True:
        print("\n================Log in================")
        id_input = input("ID: ")
        password_input = input("Password: ")
        
        if id_input == "root" and password_input == "12345678":
            return "root"
        
        with open("user_list.txt", "r") as file:
            for line in file:
                id_, password = line.strip().split("/")
                if id_ == id_input and password == password_input:
                    return "user"
        print("**Wrong password. try again.**")


def create_account():
    print("\n================sign up================")
    while True:
        new_id = input("ID : ")
        with open("user_list.txt", "r") as file:
            for line in file:
                id_, _ = line.strip().split("/")
                if id_ == new_id:
                    print("**already exists**")
                    break
            else:    
                print("Password must be 8 to 12 characters long \nand contain at least one uppercase letter, \nlowercase letter, and number.")            
                while True:
                    new_password = input("Password: ")
                    violations = []
                    if len(new_password) < 8 or len(new_password) > 12:
                        violations.append("enter within 8 to 12 characters.")
                    if not any(char.isupper() for char in new_password):
                        violations.append("include at least one capital letter.")
                    if not any(char.islower() for char in new_password):
                        violations.append("include at least one lowercase letter.")
                    if not any(char.isdigit() for char in new_password):
                        violations.append("include at least one number.")

                    if violations:
                        print("You Must")
                        for violation in violations:
                            print("-", violation)
                    else:
                        with open("user_list.txt", "a") as file:
                            file.write(f"{new_id}/{new_password}\n")
                        print("계정이 성공적으로 생성되었습니다.")
                        return


def main():
    while True:
        print("================================")
        print("\n1. Login\n2. Sign up\n3. exit")
        choice = input("select: ")

        if choice == "1":
            user_type = login()
            if user_type == "root":
                print("Login as root")
                # 관리자 기능 실행
            elif user_type == "user":
                print("Login as user")
                # 사용자 기능 실행

        elif choice == "2":
            create_account()

        elif choice == "3":
            print("exit program.")
            break

        else:
            print("**Wrong select. try again**")


if __name__ == "__main__":
    main()