""" project 1"""
import numpy as np
import os

current_file_path = os.path.realpath(__file__)  # 현재 작업 디렉토리 얻기
parent_directory = os.path.dirname(current_file_path)  # 부모 디렉토리 얻기

    
#############
class course:
    def __init__(self):
        data = []
        file = open(parent_directory + "\\basics.txt", "r")     
        for line in file:
            row = line.strip().split('\t')    #row = [item0, item2, item3, ... ]
            data.append(row)    #1차원 배열인 row를 2차원 배열 data로 변환

        arr2d = np.array(data)   # NumPy 배열로 변환합니다.
        
        file.close()
        print(arr2d) # 결과를 출력합니다.
##############


class User:
    pass


class Root:
    pass



def load_user_list():
    user_list = []
    with open(parent_directory + "\\user_list.txt", "r") as file:
        for line in file:
            id_, password = line.strip().split("/")
            user_list.append((id_, password))
    return user_list

# 로그인 구현부
def login():
    while True:
        print("\n" + " Log in ".center(40, '='))
        id_input = input("ID: ")
        password_input = input("Password: ")
        
        if id_input == "root" and password_input == "12345678": # 관리자 계정 확인
            return "root"
        
        user_list = load_user_list()
        for id_, password in user_list:
            if id_ == id_input and password == password_input:
                return "user"
        print("**Wrong password. try again.**")


# 계정 생성 구현부
def create_account():
    print("\n" + " sign up ".center(40, '='))
    while True:
        new_id = input("ID : ")
        user_list = load_user_list()
        for id_, _ in user_list:
            if id_ == new_id:
                print("**already exists**")
                break
        else:
            print(" Password Rule ".center(40, ' '))
            print("Password must be 8 to 12 characters long \nand contain at least one uppercase letter, \nlowercase letter, and number.")            
            while True:
                new_password = input("\nPassword: ")
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
                    print("\n**You Must**")
                    for violation in violations:
                        print("-", violation)
                else:
                    confirm_password = input("Please enter your password again: ")
                    if new_password != confirm_password:
                        print("**Passwords do not match. Please try again.**")
                    else:
                        with open(parent_directory + "\\user_list.txt", "a") as file:
                            file.write(f"{new_id}/{new_password}\n")
                        print("Account successfully created.")
                        return


def main():

    while True:
        print("\n" + " Menu ".center(40,'='))
        print("1. Login\n2. Sign up\n3. exit")
        choice = input("select: ")

        if choice == "1":
            user_type = login()
            if user_type == "root":
                print("-Login as root-")
                # 관리자 기능 실행 // 이거를 이제 return 받지 않고 그냥 login 함수에서 즉시 함수 호출해서 실행
            elif user_type == "user":
                print("-Login as user-")
                # 사용자 기능 실행 //이것도 마찬가지

        elif choice == "2":
            create_account()

        elif choice == "3":
            print("-exit program-")
            break

        else:
            print("**Wrong select. try again**")


if __name__ == "__main__":
    main()
