"""import module"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import numpy as np
import hashlib

#절대 경로를 얻기
current_file_path = os.path.realpath(__file__)
parent_directory = os.path.dirname(current_file_path)

def hash_password(password):
    """입력된 비밀번호를 바이트로 변환하여 SHA-256 해시 생성
    Args:
        password : 비밀번호
        
    Return:
        hashed_password : 비밀번호를 SHA-256해시 반환
    """
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    
    except Exception as e:
        print("Error : ", e)


def load_txt(file_name, mode):
    """Text 파일을 읽어 2차원 배열로 반환
    Args:
        file_name : 파일 명
        mode : 읽어올 모드 (ex> r, w)
    
    Return:
        arr2d : 파일 내용을 np 배열로 반환
    """
    try:
        data = []
        with open(parent_directory + "\\" + file_name, mode, encoding='utf-8') as file:
            for line in file:
                row = line.strip().split("\t")
                data.append(row)
        arr2d = np.array(data)
        return arr2d

    except Exception as e:
        print("Error : ", e)


def write_txt(file_name, data):
    """Text 파일에 데이터 작성
    Args:
        file_name : 파일 명
        mode : 읽어올 모드 (ex> r, w)
    """
    try:
        np.savetxt(parent_directory + "\\" + file_name, data, fmt='%s', delimiter='\t')

    except Exception as e:
        print("Error : ", e)

def destory_widget(widgets):
    """생성된 widget 제거
    Args:
        widgets : 제거할 widget
    """
    try:
        for widget in widgets.winfo_children():
            widget.destroy()

    except Exception as e:
        print("Error : ", e)

def destroy_label_frame(label_frame):
    """widget 제거 후 label_frame 제거
    Args:
        label_frame : 제거할 라벨 프레임
    """
    try:
        destory_widget(label_frame)
        label_frame.destroy()

    except Exception as e:
        print("Error : ", e)

def schedule_divide(selected_subject):
    """과목의 수업시간 전처리 함수
        Mon#B1#Wed#C1 -> ['Mon#B', 'Wed#C'], Mon#B3 -> ['MonB', 'Mon#C', 'Mon#D']
        시간표의 Row, column 으로 사용하기 위해 정수로 반환
        시간표에 출력한 text를 가공
    Args:
        selected_subject : 전처리할 과목 데이터
    
    Returns:
        time : 행 정보(A교시, B교시 ...)
        day : 요일 정보(Mon, Thu, ...)
        text : 시간표에 출력할 정보
    """
    try:
        string = selected_subject[4]
        split_data = string.split("#")
        result = [split_data[i] + '#' + split_data[i+1] for i in range(0, len(split_data), 2)]

        time = []
        day = []
        text = []
        for item in result:
            for n in range(0, int(item.split("#")[1][1])):
                time.append(ord(item.split("#")[1][0]) -ord("A") + n)
                day.append(day_change(item.split("#")[0]))
                text.append(selected_subject[1] + "\n" + selected_subject[5])

        return time, day, text

    except Exception as e:
        print("Error : ", e)

def day_change(string):
    """Mon, Thu,와 같은 요일 정보 숫자로 반환
    Args : 
        string : 숫자로 바꿀 요일 정보
    Return :
        각 요일에 따른 정수값
    """
    try:
        if "Mon" in string:
            return 0
        elif "Tue" in string:
            return 1
        elif "Wed" in string:
            return 2
        elif "Thu" in string:
            return 3
        elif "Fri" in string:
            return 4

    except Exception as e:
        print("Error : ", e)


class RootFunctions:
    """관리자 동작을 담고있는 사용자 클래스
    __init__:
        init_screen : 동작을 구현하는 프레임을 출력할 초기 화면
        md_button_frame : 로그아웃시 삭제할 프레임
        modify_button : 수정 버튼
        add_button : 추가 버튼
        delete_button : 삭제 버튼
        update_button : 업데이트 버튼
        logout_button : 로그아웃 버튼

        emptyrow : 빈 행을 추가하기 위한 리스트
        main_frame : 수강신청 목록을 출력하기 위한 프레임
        class_list_app : 수업 목록을 출력하는 클래스 선언
        """
    def __init__(self, init_screen, md_button_frame, modify_button
                 , add_button, delete_button, update_button, logout_button):
        self.subject_data = load_txt("basics.txt", "r")
        self.init_screen = init_screen
        self.md_button_frame = md_button_frame
        self.modify_button = modify_button
        self.add_button = add_button
        self.delete_button = delete_button
        self.update_button = update_button
        self.logout_button = logout_button

        self.emptyrow = ["", "","", "", "", ""]
        self.main_frame = tk.LabelFrame(init_screen, width=820, height=210, text="수강신청 목록")
        self.main_frame.grid(row=0, column=0, padx=10, pady=20)
        self.class_list_app = ClassListApp(self.main_frame, "entry", self.subject_data)
        self.create_widgets()

    def create_widgets(self):
        """관리자 모드의 위젯들의 명령어 할당"""
        try:
            self.class_list_app.dis_list()
            self.modify_button.config(command=self.toggle_modify_mode)
            self.update_button.config(command=self.update)
            self.add_button.config(command=self.add)
            self.delete_button.config(command=self.delete)
            self.logout_button.config(command=self.logout)

        except Exception as e:
            print("Error : ", e)


    def toggle_modify_mode(self):
        """수정 모드 버튼 구현
            modify_mode라는 toggle을 통하여 모드 ON/OFF 전환
            수정 모드 ON 시 수정에 필요한 버튼 표시 및 Entry를 입력 가능한 상태로 전환
            수정 모드 OFF 시 기존 버튼 구성으로 복귀
        """
        try:
            self.class_list_app.modify_mode = not self.class_list_app.modify_mode
            #수정모드 활성화 시 버튼 구성 변경 및 entry를 입력 가능한 상태로 전환
            if self.class_list_app.modify_mode:
                self.update_button.grid(row=0, column=0, padx=2, pady=5, sticky="nsew")
                self.delete_button.grid(row=1, column=0, padx=2, pady=5, sticky="nsew")
                self.add_button.grid(row=2, column=0, padx=2, pady=5, sticky="nsew")
                self.modify_button.grid_forget()
                self.class_list_app.entry_widgets=[]
                self.class_list_app.dis_list()

            #수정모드 비활성화 시 버튼 구성 변경
            else:
                self.update_button.grid_forget()
                self.delete_button.grid_forget()
                self.add_button.grid_forget()
                self.modify_button.grid(row=0, column=0, padx=2, pady=5, sticky="nsew")

        except Exception as e:
            print("Error : ", e)

    def update(self):
        """업데이트 버튼 기능 구현
            빈칸이 있다면 업데이트 X, 빈칸을 빨간색으로 표시하고 오류 메시지 출력
            데이터를 저장하기 전에 과목코드에 따라 재정렬 과정 수행
            수정된 내용을 저장하고 변수 초기화 및 수정된 정보로 화면 재 출력
        """
        def has_blank():
            try:
                for entry in self.class_list_app.entry_widgets:
                    if entry.get() == "":
                        entry.config(bg="red")
                if any(entry.get() == "" for entry in self.class_list_app.entry_widgets):
                    messagebox.showerror("Error", "빈칸이 있습니다.")
                    return True

            except Exception as e:
                print("Error : ", e)
        
        def same_code():
            """과목 코드에 중복된 값이 있는지 확인하고, 중복이 있다면 오류를 출력하는 함수"""
            try:
                codes = [entry.get() for entry in self.class_list_app.entry_widgets[::len(self.class_list_app.header)]]
                if len(codes) != len(set(codes)):
                    messagebox.showerror("Error", "중복된 과목 코드가 있습니다.")
                    return True
            except Exception as e:
                print("Error : ", e)
        #빈칸이 있다면 update 동작 X
        try:
            if has_blank():
                return
            elif same_code():
                return
            #재정렬
            self.class_list_app.subject_update()
            sorted_indices = np.argsort(self.class_list_app.subject_data[:, 0].astype(int))
            self.class_list_app.subject_data = self.class_list_app.subject_data[sorted_indices]
            #수정된 내용 저장 밑 목록 다시 출력
            write_txt("basics.txt", self.class_list_app.subject_data)
            self.class_list_app.entry_widgets=[]
            self.toggle_modify_mode()
            self.class_list_app.dis_list()

        except Exception as e:
            print("Error : ", e)

    def delete(self):
        """delete 버튼 기능 구현
            delete_mode라는 toggle을 통하여 모드 ON/OFF 전환
            delete_mode ON 시 "activate" 문구를 띄우고 빨간색으로 표시
            delete_mode OFF 시 기존 버튼으로 복귀
        """
        try:
            self.class_list_app.delete_mode = not self.class_list_app.delete_mode
            #삭제모드에 따른 Delete 버튼 내 텍스트 변경
            if self.class_list_app.delete_mode:
                self.delete_button.config(text="activate", fg="red")
                self.update_button.config(state="disabled")
            else:
                self.delete_button.config(text="Delete", fg="black")
                self.update_button.config(state="normal")

        except Exception as e:
            print("Error : ", e)

    def add(self):
        """add 버튼 기능 구현
            add 버튼을 누르면 빈 행을 마지막에 넣고 화면을 다시 출력하여 목록 마지막에 빈행 추가
        """
        try:
            #add 버튼을 누르면 마지막에 새로운 행 추가 밑 목록 갱신
            self.class_list_app.subject_update()
            self.class_list_app.subject_data = np.vstack((self.class_list_app.subject_data, self.emptyrow))
            self.class_list_app.entry_widgets=[]
            self.class_list_app.dis_list()

        except Exception as e:
            print("Error : ", e)

    def logout(self):
        """logout 버튼 기능 구현
            로그아웃시 관리자 화면을 구성하고 있는 프레임 모두 제거
        """
        try:
            destroy_label_frame(self.main_frame)
            destroy_label_frame(self.md_button_frame)
            logindesign(self.init_screen)

        except Exception as e:
            print("Error : ", e)


class UserFunctions:
    """사용자 클래스 변수 선언
    __init__:
        init_screen : 동작을 구현하는 프레임을 출력할 초기 화면
        md_buttonframe1 : 로그아웃시 삭제할 프레임
        md_buttonframe2 : 로그아웃시 삭제할 프레임
        update_time_b : 시간 갱신 버튼
        update_time_l : 남은 시간 표출 라벨
        select_button : 선택 버튼
        cancel_button : 삭제 버튼
        schedule_button : 시간표 출력 버튼
        logout_button : 로그아웃 버튼
        credit_label_frame : 수강 학점과 전필 수 표출 라벨
        name : 사용자 이름
        
        remaining_time : 남은 시간
        current_credit : 현재 신청 학점
        currnet_required : 현재 신청 전필 수
        selected_subjects : 사용자가 신청한 과목 정보
        main_frame1 : 수강 신청 목록을 표시할 프레임
        main_frame2 : 사용자의 신청 목록을 표시할 프레임
        class_list_app : 수강 신청 목록 표시를 위한 클래스 선언
        selected_list : 사용자의 신청 목록을 표시를 위한 클래스 선언
        credit_label : 신청학점 출력하기 위한 라벨
        required_label : 신청한 전필 수를 출력하기 위한 라벨
    
    """

    def __init__(self, init_screen,md_buttonframe1, md_buttonframe2, update_time_b
                 ,update_time_l, select_button, cancel_button, schedule_button
                 ,logout_button, credit_label_frame, name):
        self.subject_data = load_txt("basics.txt", "r")
        self.user_data = load_txt("user_list.txt", "r")

        self.credit_label_frame = credit_label_frame
        self.init_screen = init_screen
        self.md_buttonframe1 = md_buttonframe1
        self.md_buttonframe2 = md_buttonframe2
        self.update_time_b = update_time_b
        self.update_time_l = update_time_l
        self.select_button = select_button
        self.cancel_button = cancel_button
        self.schedule_button = schedule_button
        self.logout_button = logout_button
        self.name = name

        self.remaining_time = 5*60
        self.current_credit = 0
        self.currnet_required = 0
        self.selected_subjects = self.return_registered_data(name, self.subject_data, self.user_data)
        self.main_frame1 = tk.LabelFrame(init_screen, width=820, height=210, text="수강신청 목록")
        self.main_frame1.grid(row=0, column=0, padx=10, pady=10)
        self.main_frame2 = tk.LabelFrame(init_screen, text = "신청현황", width=820, height=210)
        self.main_frame2.grid(row=1, column=0, padx=10, pady=20)
        self.class_list_app = ClassListApp(self.main_frame1, "label", self.subject_data)
        self.selected_list = ClassListApp(self.main_frame2, "label", self.selected_subjects)
        self.credit_label = tk.Label(self.credit_label_frame, relief=tk.SOLID
                                    , width=8, height=1, borderwidth=1)
        self.credit_label.grid(row = 0, column=0, sticky="nsew", pady = 2)
        self.required_label = tk.Label(self.credit_label_frame, relief=tk.SOLID
                                    , width=8, height=1, borderwidth=1)
        self.required_label.grid(row = 1, column=0, sticky="nsew")

    #사용자 화면 구현
    def create_widgets(self):
        """수강신청 목록과 사용자의 수강신청 목록 출력 및 사용자 모드의 위젯들의 명령어 할당"""
        try:
            self.class_list_app.dis_list()
            self.selected_list.dis_list()
            self.update_label()
            self.update_time_b.config(command=self.time_reset)
            self.schedule_button.config(command=self.schedule)
            self.select_button.config(command=self.select)
            self.cancel_button.config(command=self.cancel)
            self.logout_button.config(command=self.logout)
            self.time_update()

        except Exception as e:
            print("Error : ", e)

    def time_update(self):
        """남은 시간을 관리하는 함수
            라벨에 1초 뒤 time_update를 재귀적으로 호출하여 시간 관리
            모든 시간이 지나면 로그아웃
        """
        try:
            min_, sec = divmod(self.remaining_time, 60)
            time_str = f"{min_:02d}:{sec:02d}"
            self.update_time_l.config(text = time_str)

            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.update_time_l.after(1000, self.time_update)
            else:   #수정
                self.logout()

        except Exception as e:
            print("Error : ", e)

    def time_reset(self):
        """시간 갱신 버튼을 눌러 남은 시간 초기화
            남은 시간 60*5 => 5분
        """
        self.remaining_time = 60*5


    def return_registered_code(self, user, user_data):
        """사용자 정보 데이터에서 특정 사용자 이름을 바탕으로 기존에 신청한 과목 코드 데이터 반환
        Args :
            user : 사용자 이름
            user_data :  사용자 정보
        Returns :
            신청한 과목이 있을 경우 : 맨 앞에 빈 요소 하나를 포함한 numpy배열로 된 과목 코드
            신청한 과목이 없을 경우 : 빈 numpy배열
        """
        try:
            indice = np.where(user_data == user)[0]
            indice_int = indice[0]

            code = user_data[indice_int][2]
            if user_data[indice_int][2] == "/":
                code = user_data[indice_int][2].replace("/", "")

            existed_subject = code.split("/")
            return np.array(existed_subject)
        
        except Exception as e:
            print("Error : ", e)
    

    def return_registered_data(self, user, subject_data, user_data):
        """과목 코드를 통해 신청한 과목에 대한 전체 데이터 반환
            return_registered_code를 사용해서 사용자가 신청한 과목 코드 확인
            해당 정보를 바탕으로 사용자가 신청한 과목에 대한 정보를 넘파이 배열로 반환
            신청한 과목이 없다면 명시적으로 None 반환
        Args : 
            user : 사용자 이름
            subject_data : 수강신청 정보
            user_data : 사용자 정보
        Returns :
            신청한 과목이 존재하면 : data[1:]
            신청한 과목이 없다면 : None
        """
        try:
            registered_code = self.return_registered_code(user, user_data)[1:]
            indice = np.where(np.isin(subject_data, registered_code))[0]
            data = np.array([None, None, None, None, None, None])

            #과목이 비어있다면 None을 return 그렇지 않다면 과목 정보 반환
            if len(indice):
                for idx in indice:
                    data = np.vstack([data, subject_data[idx]])
                return data[1:]
            return None

        except Exception as e:
            print("Error : ", e)

    def init_cal(self):
        """초기 클래스 생성시 신청 학점과 신청한 전필 수를 계산하여 저장하는 함수
            신청한 과목의 학점을 모두 합하여 계산
            신청한 과목이 전필일때 1을 더하여 신청한 전필 수 계산
        """
        try:
            credit = 0
            required = 0
            if self.selected_subjects is not None:
                for subject in self.selected_subjects:
                    credit += int(subject[3])
                    if subject[2] == "Required":
                        required += 1
            self.current_credit = credit
            self.currnet_required = required

        except Exception as e:
            print("Error : ", e)

    def update_label(self):
        """신청한 학점과 신청한 전필수를 업데이트하여 출력하는 함수
            신청한 전필수가 4 이상이여야 함으로 4보다 작다면 빨간색으로 표시
        """
        try:
            self.init_cal()
            self.credit_label.config(text = f"학점 : {self.current_credit}")
            self.required_label.config(text = f"전필 : {self.currnet_required}", fg='black')
            if self.currnet_required < 4:
                self.required_label.config(fg='red')

        except Exception as e:
            print("Error : ", e)

    def select(self):
        """수강 목록에서 수업을 신청을 처리하는 함수
            if 사용자가 신청한 목록이 없다면 : 바로 추가
            else if선택한 항목을 신청하였을 때 최대 학점을 초과한다면 : 오류 메시지 출력
            else if선택한 항목을 신청하였을 때 이미 존재하는 수업과 겹친다면 : 오류 메시지 출력
            else 유효한 수강신청 목록이므로 마지막에 추가

            수강신청이 끝나면 화면 업데이트 및 txt 파일 수정
        """
        
        def schedule_overlap():
            """기존 수업과 중복이 있는지 확인하는 함수
                schedule_divide 함수를 통해 신청할 수업 시간을 전처리
                schedule_divide 함수를 사용하여 기존에 있던 수업과 비교하여 교집합이 있다면 중복
            """
            try:
                times, days, _ = schedule_divide(self.class_list_app.selected_data)
                temp = [f"{time}{day}" for time, day in zip(times, days)]

                #사용자의 수강신청 정보를 토대로 중복 검사
                for subject in self.selected_subjects:
                    times, days, _ = schedule_divide(subject)
                    if np.intersect1d([f"{time}{day}" for time, day in zip(times, days)], temp).size:
                        return True
                    
            except Exception as e:
                print("Error : ", e)
        
        try:
            #수강신청한 항목이 없다면
            if self.current_credit + int(self.class_list_app.selected_data[3]) > 17:
                messagebox.showinfo("학점 초과", "신청 가능한 최대 학점을 초과하였습니다.")
                return
            elif self.selected_subjects is None:
                self.selected_subjects = np.array([self.class_list_app.selected_data])
            elif schedule_overlap():
                messagebox.showinfo("시간 중복", "같은 시간에 이미 수업이 있습니다")
                return
            else:
                self.selected_subjects = np.vstack([self.selected_subjects, self.class_list_app.selected_data])

            #신청에 성공하였다면 업데이트 실시
            self.selected_list.subject_data = self.selected_subjects
            self.selected_list.entry_widgets = []
            self.write(self.selected_subjects, self.user_data, self.name)
            self.update_label()
            self.selected_list.dis_list()

        except Exception as e:
            print("Error : ", e)

    def cancel(self):
        """신청한 항목에서 수강 취소시 호출되는 함수
            신청 목록에서 선택한 항목을 제거하고 화면을 업데이트 및 txt 파일 수정
        """
        try:
            self.selected_subjects = np.delete(self.selected_subjects, self.selected_list.selected_row, axis=0)
            self.selected_list.subject_data = self.selected_subjects
            self.selected_list.entry_widgets = []
            self.write(self.selected_subjects, self.user_data, self.name)
            self.update_label()
            self.selected_list.dis_list()

        except Exception as e:
            print("Error : ", e)

    def collect(self, selected_subjects):
        """user_list의 형식에 맞춰 과목코드 수정
            user_list 파일에 저장할 형식에 맞춰 저장 (/100/101/102/)
        Args : 
            selected_subjects : 사용자가 수강신청한 목록

        Returns :
            형식에 맞춰 변환한 신청환 과목 정보
        """
        try:
            result = '/'.join([item[0] for item in selected_subjects])
            return '/' + result

        except Exception as e:
            print("Error : ", e)

    def write(self, selected_subjects, user_list, name):
        """신청한 과목코드 수정 후 Write
            유저 정보에서 collect 함수를 통해 처리된 과목코드를 이름을 통해 찾아 수정
            작성이 유효하지 않다면 치명적인 오류 발생으로 logout
        Args : 
            selected_subjects : 사용자가 수강신청한 목록
            user_list : 사용자 목록
            name : 사용자 이름           
        """
        try:
            #사용자의 이름에 해당하는 위치 확인
            for index, user_data in enumerate(user_list):
                if user_data[0] == name:
                    user_list[index][2] = self.collect(selected_subjects)
                    write_txt("user_list.txt", user_list)
                    return
            #오류 발생
            self.logout()

        except Exception as e:
            print("Error : ", e)

    def logout(self):
        """로그아웃 구현
            로그아웃시 전필과목을 4개 이상 신청하지 않았다면 오류 출력
            로그아웃시 존재하던 프레임 전부 학제후 로그인 화면 출력
        """
        try:
            #기존에 존재하던 프레임 제거 후 로그인 화면 호출
            if self.currnet_required < 4:
                result = messagebox.askquestion("확인", "전필 수업은 4개 이상 수강하여야 합니다. 그래도 로그아웃 하시겠습니까?")
                if result == "no":
                    return

            destroy_label_frame(self.main_frame1)
            destroy_label_frame(self.main_frame2)
            destroy_label_frame(self.md_buttonframe1)
            destroy_label_frame(self.md_buttonframe2)

            logindesign(self.init_screen)

        except Exception as e:
            print("Error : ", e)

    def schedule(self):
        """시간표 출력 함수
        시간표 출력 시 시간표 출력 클래스를 선언하여 시간표 출력
        """
        try:
            #시간표 요청시 시간표 클래스를 통하여 시간표 출력
            self.schedule_frame = tk.Toplevel(self.init_screen)
            self.my_schedule = Myschedule(self.schedule_frame, self.selected_subjects)

            self.my_schedule.frame()
            self.my_schedule.create_labels()

        except Exception as e:
            print("Error : ", e)


class ClassListApp:
    """수업 목록 표시에 대한 클래스
    Args :
        self.modify_mode : 수정 모드에 대한 논리 변수 toggle
        self.delete_mode = 삭제 모드에 대한 논리 변수 toggle
        self.main_frame : 목차와 목록들을 표시할 프레임
        self.mode : 목록을 label로 만들지 entry로 만들지 결정
        self.subject_data : 목록에 출력할 데이터
        self.original_bg_color : 시스템의 배경화면 색
        self.entry_widgets : 출력된 목록 정보(목록과의 상호작용을 위해 사용)
        self.selected_data : 선택된 데이터 정보(handle_click에 사용)
        self.selected_row : 선택된 데이터의 행정보(handle_click에 사용)
        self.header : 목차 생성을 위한 리스트
        self.header_size : 목차 생성시 너비를 설정하기 위한 튜플
    """
    def __init__(self, main_frame, mode, data):
        self.modify_mode = False
        self.delete_mode = False
        self.main_frame = main_frame
        self.mode = mode
        self.subject_data = data
        self.original_bg_color = main_frame.cget("background")  # 원래의 배경색 저장
        self.entry_widgets = []
        self.selected_data = []
        self.selected_row = []
        self.header = ("과목번호", "과목명", "전필여부", "학점", "수업 시간", "수업 장소")
        self.header_size = (12, 30, 12, 8, 20, 20)

    def dis_list(self):
        """수업 목록을 표시하는 함수
            기존에 있던 메인 프레임을 삭제하고 다시 목차와 목록 출력
            dis_label_frame을 통해 목차 생성
            dis_canvas를 통해 목록 생성
        """

        def dis_label_frame():
            """목차 생성 프레임"""
            try:
                label_frame = tk.Frame(self.main_frame, width=700, pady=5)
                label_frame.pack(side="top", anchor="nw")

                for i, column in enumerate(self.header):
                    label = tk.Label(label_frame, width=self.header_size[i]
                                    , relief=tk.RIDGE, text = column)
                    label.grid(row=0, column=i + 1, padx=1, pady=1, sticky="nsew")
                    
            except Exception as e:
                print("Error : ", e)

        def dis_canvas():
            """목록 생성 프레임
                목록에 스크롤바를 연결하기 위해 canvas를 사용
                canvas 위에 label_or_entry 함수를 통해 label 혹은 entry로 목록을 생성하고 스크롤바를 연결
                canvas 내 요소들에 따라 canvas 사이즈 조정
                """
            try:
                canvas = tk.Canvas(self.main_frame, height=160, width=790, highlightthickness=0)
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
                inner_frame = tk.Frame(canvas)
                canvas.create_window((0, 0), window=inner_frame, anchor="nw")

                scrollbar = ttk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                canvas.configure(yscrollcommand=scrollbar.set)

                if self.subject_data is not None:
                    label_or_entry(inner_frame)

                inner_frame.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))
                scrollbar.place(relx=1, rely=0, relheight=1, relwidth=0.03, anchor='ne')
                scrollbar.config(command=canvas.yview)

            except Exception as e:
                print("Error : ", e)

            #목록을 Label 혹은 Entry로 생성하는 함수
        def label_or_entry(inner_frame):
            """목록을 Label 혹은 Entry로 생성하는 함수
                반복문을 돌며 수업 목록(subject_data)을 생성
                Label일때와 Entry일 때를 구분하여 event를 할당
                Label일때 
                    Label로 생성 및 handel_click 함수 연결
                Entry 일때
                    Entry로 생성 및 handel_double_click 함수 연결
                    수정 모드가 아니면 읽기모드로 전환

            Args :
                inner_frame : 목록을 출력할 프레임
            """
            try:
            #반복문을 돌며 label 생성
                for i, row in enumerate(self.subject_data):
                    for j, value in enumerate(row):
                        #Entry 생성을 원할 때
                        if self.mode == "entry":
                            entry = tk.Entry(inner_frame, width=self.header_size[j]
                                            , relief=tk.RIDGE, borderwidth=2)
                            entry.insert(tk.END, value)
                            if not self.modify_mode:
                                entry.config(state="readonly")
                            entry.bind("<Double-Button-1>", lambda event
                                    , widget=entry: self.handle_double_click(widget))
                        #Label 생성을 원할 때
                        elif self.mode == "label":
                            entry = tk.Label(inner_frame, width=self.header_size[j]
                                            , relief=tk.RIDGE,text=value, borderwidth = 2
                                            , bg=self.original_bg_color)
                            entry.bind("<Button-1>", lambda event, widget=entry
                                    :self.handle_click(widget))
                        entry.grid(row=i, column=j + 1, padx=1, pady=1, sticky="nsew")
                        self.entry_widgets.append(entry)

            except Exception as e:
                print("Error : ", e)
        try:
            destory_widget(self.main_frame)
            dis_label_frame()
            dis_canvas()

        except Exception as e:
            print("Error : ", e)

    def handle_click(self, widget):
        """Label로 생성시 목록을 눌렀을 때 이벤트 함수
            한번에 한 행만 선택하도록 이전에 선택된 행이 있으면 선택을 해제
            선택된 항목의 행을 계산하여 해당하는 행들을 파란색으로 표시
            해당 행의 정보를 selected_data에 저장하고 selected_row에는 선택된 행 정보 저장
        Args :
            widget : 출력된 목록의 요소들
        """
        try:
            for idx in self.selected_row:
                for entry_widget in self.entry_widgets[idx * len(self.header): (idx + 1) * len(self.header)]:
                    entry_widget.config(bg=self.original_bg_color)
            self.selected_row.clear()


            index = self.entry_widgets.index(widget)
            row_index = index // len(self.header)
            start_index = row_index * len(self.header)
            end_index = start_index + len(self.header)

            for entry_widget in self.entry_widgets[start_index:end_index]:
                entry_widget.config(bg="#99CCFF")

            self.selected_data = self.subject_data[row_index]
            self.selected_row.append(row_index)

        except Exception as e:
            print("Error : ", e)

    def handle_double_click(self, widget):
        """Entry로 생성시 목록을 눌렀을 때 발생하는 이벤트 함수
            수정 모드이고 삭제 모드일 때 더블클릭하면 더블클릭한 목록의 행 계산
            사용자에게 삭제 유무를 확인받음
            삭제 요청시 subject_update를 통해 수정된 정보를 저장하고 삭제 진행
            삭제 후 entry_widgets 초기화 및 화면 업데이트
        Args :
            widget : 출력된 목록의 요소들
        """
        try:
            if self.modify_mode and self.delete_mode:
                index = self.entry_widgets.index(widget)
                row_index = index // len(self.header)
                confirmation = messagebox.askokcancel("Delete", "삭제하겠습니까?")
                if confirmation:
                    self.subject_update()
                    self.subject_data = np.delete(self.subject_data, row_index, axis=0)
                    self.entry_widgets=[]
                    self.dis_list()

        except Exception as e:
            print("Error : ", e)

    def subject_update(self):
        """변경된 데이터를 임시로 저장하는 함수
            현재 entry에 저장된 내용을 바탕으로 과목 정보 수정
        """
        try:
            temp_data = []
            for i in range(len(self.subject_data)):
                row_data = [entry.get() for entry in self.entry_widgets[i * len(self.header):(i + 1) * len(self.header)]]
                temp_data.append(row_data)
            self.subject_data = np.array(temp_data)

        except Exception as e:
            print("Error : ", e)



class Myschedule:
    """시간표를 출력하기 위한 클래스
        self.selected_subject : 시간표로 바꿀 사용자의 수강신청 목록
        self.scheduleframe : 시간표를 출력하기위한 자식 프레임
    """
    def __init__(self, schedule_frame, selected_subject):
        self.selected_subject = selected_subject
        self.scheduleframe = schedule_frame

    def frame(self):
        """시간표 출력을 위한 격자 생성"""
        try:
            for i in range(10):
                for j in range(7):
                    label = tk.Label(self.scheduleframe, text = None, borderwidth=1, relief="solid", width=15, height=2)
                    if i ==0:
                        label.grid(row=i, column=j, rowspan= 1, sticky="nsew")
                    else:
                        label.grid(row=3*(i-1)+1, column=j, rowspan= 3, sticky="nsew")

        except Exception as e:
            print("Error : ", e)

    def data_processes(self):
        """시간표 출력에 필요한 행, 열, 출력 데이터 가공
            반복문을 통해 리스트에 계속해서 추가

        Returns :
            divide_row : 행 정보
            divide_col : 열 정보
            text : 가공된 데이터 리스트
        """
        try:
            divide_row = []
            divide_col = []
            text = []
            for subject in self.selected_subject:
                row_temp, col_temp, text_temp = schedule_divide(subject)
                divide_row.extend(row_temp)
                divide_col.extend(col_temp)
                text.extend(text_temp)

            return divide_row, divide_col, text
        
        except Exception as e:
            print("Error : ", e)

    def display(self, row, col, data):
        """과목 출력"""
        try:
            label = tk.Label(self.scheduleframe, text = data, borderwidth=1, relief="solid"
                            , width=15, height=2, bg="#F2F4EC")
            label.grid(row= 3*row+1, column= col+2, sticky="nsew", rowspan=3)

        except Exception as e:
            print("Error : ", e)

    def create_labels(self):
        """요일, 수업시간(알파벳 형식, 시간 형식) 프레임 생성"""
        try:
            weekday = list("  월화수목금")
            for i in range(7):
                label = tk.Label(self.scheduleframe, text = weekday[i], borderwidth=1, relief="solid"
                                , width=15, height=2, bg="#F2F4EC")

                label.grid(row=0, column=i, rowspan= 1, sticky="nsew")

            alphabet_time = list("ABCDEFGHI")
            for i in range(9):
                label = tk.Label(self.scheduleframe, text = alphabet_time[i], borderwidth=1
                                , relief="solid", width=10, height=6, bg="#F2F4EC")

                label.grid(row= 1 + 3*i, column=0, rowspan= 3, sticky="nsew")

            time = [f"{hour:02d}:{minute:02d}" for hour in range(9, 23) for minute in [0, 30]]
            for i in range(27):
                label = tk.Label(self.scheduleframe, text = time[i], borderwidth=1, relief="solid"
                                , width=10, height=2 , bg="#F2F4EC")

                label.grid(row= 1 + i, column= 1, rowspan= 1, sticky="nsew")

            row, col, text_data = self.data_processes()
            for r, c, text in zip(row, col, text_data):
                self.display(int(r), int(c), text)

        except Exception as e:
            print("Error : ", e)


def root_screen(init_screen):
    """관리자 화면 출력 함수
        관리자 화면에 맞춰 사이즈 조정하고 화면을 구성
        RootFunctions 클래스를 선언하여수업 목록 출력
    Args : 
        init_screen : 관리자 화면을 출력하기 위한 초기 프레임
    """
    try:
        init_screen.geometry("890x260")
        init_screen.title("Login as " + "Root")

        md_button_frame = tk.Frame(init_screen)
        md_button_frame.grid(row=0, column=1, pady=10, sticky="nsew")
        for i in range(0,7):
            tk.Label(md_button_frame).grid(row=i, column=0, padx=2, pady=5)

        # Modify 버튼 추가
        modify_button = tk.Button(md_button_frame, text="Modify", width=6)
        modify_button.grid(row=1, column=0, padx=2, pady=5, sticky="nsew")
        # Add 버튼 추가
        add_button = tk.Button(md_button_frame, text="Add", width=6)
        # Delete 버튼 추가
        delete_button = tk.Button(md_button_frame, text="Delete", width=6)
        update_button = tk.Button(md_button_frame, text="Update", width=6)
        logout_button = tk.Button(md_button_frame, text="logout", width=6)
        logout_button.grid(row=6, column=0, padx=2, pady=5, sticky="s")

        root_func = RootFunctions(init_screen, md_button_frame,  modify_button
                                , add_button, delete_button, update_button, logout_button)
        root_func.create_widgets()

    except Exception as e:
        print("Error : ", e)

def user_screen(name, init_screen):
    """사용자 화면 출력 함수
        사용자 화면에 맞춰 사이즈 조정하고 화면을 구성
        RootFunctions 클래스를 선언하여수업 목록 출력
    Args : 
        init_screen : 관리자 화면을 출력하기 위한 초기 프레임
    """
    try:
        init_screen.geometry("890x520")
        init_screen.title("Login as " + name)

        md_button_frame1 = tk.Frame(init_screen)
        md_button_frame1.grid(row=0, column=1, pady=10, sticky="nsew")
        md_button_frame1.grid_rowconfigure(0,minsize=40)
        md_button_frame1.grid_rowconfigure(1,minsize=40)
        update_time_b = tk.Button(md_button_frame1, text="⟳")
        update_time_b.grid(row=0, column=1, padx=2, pady=5, sticky="n")
        update_time_l = tk.Label(md_button_frame1, text="")
        update_time_l.grid(row=0, column=0, padx=2, pady=5, sticky="n")
        select_button = tk.Button(md_button_frame1, text="신청", width=6, height=1)
        select_button.grid(row=1, column=0, padx=2, pady=5, sticky="s", columnspan=2)

        md_button_frame2 = tk.Frame(init_screen)
        md_button_frame2.grid(row=1, column=1, pady=20, sticky="nsew")

        cancel_button = tk.Button(md_button_frame2, text="취소", width=6, height=1)
        cancel_button.grid(row=1, column=0, padx=2, pady=5, sticky="n")
        schedule_button = tk.Button(md_button_frame2, text="시간표", width=6, height=1)
        schedule_button.grid(row=2, column=0, padx=2, pady=5, sticky="n")
        md_button_frame2.grid_rowconfigure(2,minsize=70)
        logout_button = tk.Button(md_button_frame2, text="로그아웃", width=6, height=1)
        logout_button.grid(row=4, column=0, padx=2, pady=5, sticky="s")
        credit_label = tk.Frame(md_button_frame2)
        credit_label.grid(row=0, column=0, pady=20, sticky="s")

        user_func = UserFunctions(init_screen, md_button_frame1, md_button_frame2, update_time_b,
                                update_time_l, select_button, cancel_button, schedule_button,
                                logout_button, credit_label, name)
        user_func.create_widgets()

    except Exception as e:
        print("Error : ", e)

def create_account(init_screen):
    """계정 생성 함수
        로그인 프레임을 부모로 두고 자식 프레임을 선언
        createaccountdesign을 통해 화면 구성
    Args :
        init_screen  : 부모 프레임
    """
    try:
        create_account_window = tk.Toplevel(init_screen)
        create_account_window.title("로그인")
        create_account_window.geometry("420x220")
        create_account_window.resizable(False, False)
        createaccountdesign(create_account_window)

    except Exception as e:
        print("Error : ", e)

def createaccountdesign(create_account_window):
    """계정생성 화면 디자인 구현 및 함수 구현
        화면을 구성하고 버튼에 대한 함수 연결

    Args :
        create_account_window : 계정생성 화면을 구성하기 위한 프레임
    """

    def rename_id():
        """아이디 수정 함수 구현
            아이디 중복검사 후 아이디를 다시 수정할 때
            기존 버튼형식으로 형식 및 함수 변경
        """
        try:
            nonlocal create_account_button, new_id_entry, check_id_button
            id_status_label.config(text="", fg="black")
            new_id_entry.config(state=tk.NORMAL)
            create_account_button.config(state=tk.DISABLED)
            check_id_button.config(text="중복 확인", command=check_id_duplicate)

        except Exception as e:
            print("Error : ", e)

    def check_id_duplicate():
        """아이디 중복 검사 함수 구현
            아이디 입력 entry가 비어있으면 오류 출력 
            user_list에서 ID가 이미 존재한다면 오류 출력
            없는 아이디라면 계정 생성 버튼을 활성화 하고 유요한 아이디임을 출력
        """
        try:
            nonlocal create_account_button, new_id_entry, check_id_button
            new_id = new_id_entry.get()
            #아이디 미 입력시
            if not new_id:
                id_status_label.config(text="아이디를 입력해주세요.", fg="red")
                id_status_label.after(2000, lambda: id_status_label.config(text=""))
                return
            #기존 정보에서 아이디 검사
            user_list = load_txt("user_list.txt", "r").tolist()
            for id_, _, _ in user_list:
                if id_ == new_id:
                    id_status_label.config(text="이미 존재하는 아이디입니다.", fg="red")
                    new_id_entry.config(state=tk.NORMAL)
                    return

            id_status_label.config(text="사용 가능한 아이디입니다.", fg="green")
            new_id_entry.config(state=tk.DISABLED)
            create_account_button.config(state=tk.NORMAL)
            create_account_button.config(state=tk.ACTIVE)
            check_id_button.config(text="Rename ID", command=rename_id)

        except Exception as e:
            print("Error : ", e)

    def build_new_password(confirm_password, new_password, new_id):
        """비밀번호 생성시
            비밀번호가 서로 일치하지 않는다면 비밀번호 오류 출력
            비밀번호가 조건에 맞지 않으면 조건과 일치하지 않는 내용 전부 출력
            비밀번호 조건 :
                8~12자리 이상
                대문자 1개 이상 포함
                소문자 1개 이상 포함
                숫자 1개 이상 포함
            비밀번호 조건에 일치하면 user_list.txt에 id, password 입력
        """
        try:
            if new_password != confirm_password:
                password_conditions_label.config(text="비밀번호가 일치하지 않습니다.", fg="red")
                return
            else:
                password_conditions_label.config(text="")

            violations = []
            if len(new_password) < 8 or len(new_password) > 12:
                violations.append("비밀번호는 8~12자리여야 합니다.")
            if not any(char.isupper() for char in new_password):
                violations.append("비밀번호는 대문자를 1개 이상 포함해야 합니다.")
            if not any(char.islower() for char in new_password):
                violations.append("비밀번호는 소문자를 1개 이상 포함해야 합니다.")
            if not any(char.isdigit() for char in new_password):
                violations.append("비밀번호는 숫자를 1개 이상 포함해야 합니다.")

            if violations:
                password_conditions_label.config(text="\n".join(violations), fg="red")
                return
            else:
                password_conditions_label.config(text="", fg="red")

            with open(parent_directory + "\\user_list.txt", "a", encoding='utf-8') as file:
                file.write(f"{new_id}" + "\t" + hash_password(new_password) + "\t" +"/" + "\n")
            messagebox.showinfo("성공", "성공적으로 계정을 생성하였습니다.")
            create_account_window.destroy()
            
        except Exception as e:
            print("Error : ", e)

    def handle_create_account():
        """계정생성 버튼을 누르면 entry에 적힌 데이터 저장 및 build_new_password 함수를 통해 계정 생성 과정 수행"""
        try:
            new_id = new_id_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()


            build_new_password(confirm_password, new_password, new_id)

        except Exception as e:
            print("Error : ", e)

    try:
        #계정 생성 화면 구현
        new_id_label = tk.Label(create_account_window, text="ID:")
        new_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        new_id_entry = tk.Entry(create_account_window)
        new_id_entry.grid(row=0, column=1, padx=10, pady=5)
        check_id_button = tk.Button(create_account_window, text="아이디 중복 검사"
                                    , command=check_id_duplicate, width=14)
        check_id_button.grid(row=0, column=2, padx=10, pady=5)
        new_password_label = tk.Label(create_account_window, text="Password:")
        new_password_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        new_password_entry = tk.Entry(create_account_window, show="*")
        new_password_entry.grid(row=1, column=1, padx=10, pady=5)
        id_status_label = tk.Label(create_account_window, text="", fg="black")
        id_status_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        confirm_password_label = tk.Label(create_account_window, text="중복 확인:")
        confirm_password_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        confirm_password_entry = tk.Entry(create_account_window, show="*")
        confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)
        init_text = "비밀번호는 8~12자리여야 하며 대문자, 소문자, 숫자를 1개 이상 포함하여야 합니다.."
        password_conditions_label = tk.Label(create_account_window, text=init_text
                                            , fg="red", wraplength=400, height=4)
        password_conditions_label.grid(row=3, columnspan=3, padx=10, pady=5)
        create_account_button = tk.Button(create_account_window, text="계정 생성"
                                        , command=handle_create_account, state=tk.DISABLED)
        create_account_button.grid(row=4, columnspan=3, padx=10, pady=5)

    except Exception as e:
        print("Error : ", e)


# 초기 화면 구성
def initial_login_screen():
    """초기 화면 구성
        Login Design을 출력하여 로그인 화면 호출
        init_screen을 기준으로 mainloop 실행
    """
    try:
        init_screen = tk.Tk()
        init_screen.resizable(False, False)

        logindesign(init_screen)
        init_screen.mainloop()

    except Exception as e:
        print("Error : ", e)

#로그인 구현
def logindesign(init_screen):
    """로그인 구현
        화면의 사이즈를 조절하고 로그인 화면 구성 및 버튼에 함수 연결
    """

    def handle_login():
        """로그인 요청시 entry에서 값을 읽어오고 try_login을 통해 로그인 시도"""
        try:
            id_input = id_entry.get()
            password_input = password_entry.get()
            try_login(id_input, password_input)

        except Exception as e:
            print("Error : ", e)

    def try_login(id_input, password_input):
        """로그인 시도
            관리자 계정인지 확인 후 user_list를 통해 사용자 계정인지 확인
            관리자도 사용자도 아니라면 오류 출력
        """
        try:
            user_list = load_txt("user_list.txt", "r").tolist()
            for i, (id_, password, _) in enumerate(user_list):
                if id_ == id_input and password == hash_password(password_input):
                    if not i:
                        initial_frame.destroy()
                        root_screen(init_screen)
                    else:
                        initial_frame.destroy()
                        user_screen(id_, init_screen)
                    return
            login_conditions_lable.config(text="잘못된 비밀번호입니다.", fg="red")
            login_conditions_lable.after(2000, lambda: login_conditions_lable.config(text=""))

        except Exception as e:
            print("Error : ", e)

    try:
        #로그인 화면 구성
        init_screen.geometry("280x120")
        init_screen.title("login")
        initial_frame = tk.Frame(init_screen)
        initial_frame.grid(row=0, column=0, padx=10, pady=10)

        id_label = tk.Label(initial_frame, text="ID:")
        id_label.grid(row=0, column=0, sticky="e")
        id_entry = tk.Entry(initial_frame)
        id_entry.grid(row=0, column=1, columnspan=2)
        id_entry.focus_set()
        password_label = tk.Label(initial_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="e")
        password_entry = tk.Entry(initial_frame, show="*")
        password_entry.grid(row=1, column=1, columnspan=2)
        login_button = tk.Button(initial_frame, text="Login", width=7, command=handle_login)
        login_button.grid(row=2, column=2, pady=5)
        signup_button = tk.Button(initial_frame, text="Sign Up"
                                , width=7, command=lambda: create_account(init_screen))
        signup_button.grid(row=2, column=1, pady=5)
        login_conditions_lable = tk.Label(initial_frame, text="")
        login_conditions_lable.grid(row=3, column=1, pady=5, columnspan=2)

    except Exception as e:
        print("Error : ", e)

# 관리자 계정 정보
ROOT_ID = "1"
ROOT_PASSWORD = "1"

try:
    file_name = parent_directory + "\\" + "user_list.txt"
    if not os.path.exists(file_name):
        # user_list.txt 파일을 쓰기 모드로 열어서 비어있는 파일 생성
        with open(file_name, "w") as file:
            pass  # 파일 내용을 비움
            file.write(f"{ROOT_ID}" + "\t" + hash_password(ROOT_PASSWORD) + "\t" +"/" + "\n")
        print("새로운 파일을 생성했습니다:", file_name)
    else:
        print("파일이 이미 존재합니다:", file_name)

except Exception as e:
    print("Error : ", e)

#start
initial_login_screen()
