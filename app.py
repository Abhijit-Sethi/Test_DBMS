import streamlit as st
import pandas as pd
import psycopg2
from datetime import date

#DB Mgmt
# Initialize connection.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets.postgres)
    # return psycopg2.connect(dbname="timetable",user="postgres",password="postgres",host="localhost",port=5432)
    #return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
cur=conn.cursor()
conn.autocommit=True

def fetch_duty_type():
    cur.execute("Select Duty_type from Duties;")
    rows= list(cur.fetchall())
    return rows

def fetch_subcode(sem):
    cur.execute("SELECT subject_code from Sub_code_name where sem=%s;",(sem,))
    rows= list(cur.fetchall())
    return rows

def fetch_initials():
    cur.execute("SELECT initials from faculty_details;")
    rows= list(cur.fetchall())
    return rows


today = date.today()
st.text(str(today))
month = str(today).split("-")[1]
odd_sem_menu = ["1","3","5","7"]
even_sem_menu = ["2","4","6","8"]
days_of_the_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
time_slots = ["8:15 - 9:15", "9:15 - 10:15","10:45 - 11:45","11:45 - 12:45","1:30 - 2:30","3:30 - 3:45","3:45 - 4:45",'Other...']
st.title('PES University')

pages_menu = ["Home","Subjects","Faculty Details","Faculty Subject","Designation Rank","Duties","Theory Faculty Timetable Entry","Lab Faculty Timetable Entry","Faculty Duties","About"]
page_choice = st.sidebar.selectbox("Menu",pages_menu)

if page_choice == pages_menu[0]:
    st.subheader("Home")
    st.subheader('Faculty Duties and Workload management')

if page_choice == pages_menu[1]:
    st.subheader("Add Subjects")
    if(int(month) > 6):
        sem = st.selectbox("Semester",odd_sem_menu)
    else:
        sem = st.selectbox("Semester",even_sem_menu)
    sub_code = st.text_input("Enter SUbject Code","")
    sub_name = st.text_input("Enter Subject Name","")

    if st.button("Add Data"):
        cur.execute("INSERT into Sub_code_name VALUES (%s,%s,%s);",(sem,sub_code,sub_name,))
        st.text("Data added")

    if st.button("Show data"):
        cur.execute("SELECT * from sub_code_name")
        rows=cur.fetchall()
        # st.write(rows)
        #df=pd.DataFrame(rows,columns=('Sem','Subject Code','subject name',''))
        # st.write('Sem','Subject Code','subject name','')
        #st.table(df)
        for i in range(len(rows)):
            col1, col2= st.columns([1,1])
            with col1:
                st.write(rows[i])
            with col2:
                st.button(f'Delete row{i}')
            
            

if page_choice == pages_menu[2]:
    st.subheader("Faculty Details")
    Initials = st.text_input("Initials","")
    Fac_name = st.text_input("Faculty Name","")
    Ph_no = st.text_input("Phone Number","")
    email = st.text_input("E-mail","")
    Address = st.text_input("Address","")
    Rank = st.selectbox("Designation",["Prof","Associate Prof","Assistant Prof","HOD","Chairperson","Lab Assistant","Lab in-charge"])
    
    if st.button("Add Data"):
        cur.execute("INSERT into Faculty_details VALUES (%s,%s,%ld,%s,%s,%s);",(Initials,Fac_name,Ph_no,email,Address,Rank,))
        st.text("Data added")
    if st.button("Show data"):
        cur.execute("SELECT * from sub_code_name")
        rows=cur.fetchall()
        # st.write(rows)
        #df=pd.DataFrame(rows,columns=('Sem','Subject Code','subject name',''))
        # st.write('Sem','Subject Code','subject name','')
        #st.table(df)
        for i in range(len(rows)):
            col1, col2= st.columns([1,1])
            with col1:
                st.write(rows[i])
            with col2:
                st.button(f'Delete row{i}')
            
    

if page_choice == pages_menu[3]:
    st.subheader("Faculty Subjects")
    initials = st.selectbox("Initials",fetch_initials())
    if(int(month) > 6):
        sem = st.selectbox("Semester",odd_sem_menu)
    else:
        sem = st.selectbox("Semester",even_sem_menu)
    sub_code = st.selectbox("Enter SUbject Code",fetch_subcode(sem))
    sec = st.text_input("Section","")
    
    if st.button("Add Data"):
        cur.execute("INSERT into Faculty_subject VALUES (%s,%s,%s,%s);",(sub_code,sem,sec,initials,))
        st.text("Data added")
    if st.button("Show data"):
        cur.execute("SELECT * from sub_code_name")
        rows=cur.fetchall()
        # st.write(rows)
        #df=pd.DataFrame(rows,columns=('Sem','Subject Code','subject name',''))
        # st.write('Sem','Subject Code','subject name','')
        #st.table(df)
        for i in range(len(rows)):
            col1, col2= st.columns([1,1])
            with col1:
                st.write(rows[i])
            with col2:
                st.button(f'Delete row{i}')
        # Add query to insert
        pass
# REMOVE THIS!
if page_choice == pages_menu[4]:
    st.subheader("Designation Ranks")
    Designation = st.text_input("Designation","")
    Rank = st.text_input("Rank","")
    if st.button("Submit"):
        # Query to add data
        pass

if page_choice == pages_menu[5]:
    st.subheader("Duties")
    duty_type = st.text_input("Duty type","")
    duty_priority = st.text_input("Duty Priority","")
    duty_paid = st.selectbox("Paid or unpaid",['yes','no'])
    if(duty_paid == 'yes'):
        amount = st.text_input("Enter amount","")

    if st.button("Add Duty"):
        # Query to add data
        pass


if page_choice == pages_menu[6]:
    st.subheader("Theory Faculty Timetable")
    
    if(int(month) > 6):
        sem = st.selectbox("Semester",odd_sem_menu)
    else:
        sem = st.selectbox("Semester",even_sem_menu)
		
    section = st.text_input("Section","")
    
    
    
    day = st.selectbox("Day of the week to update timetable",days_of_the_week)
    
    timing = st.selectbox("Time Slot",time_slots)
    
    if timing == 'Other...':
        start_tm = st.text_input("Starting time")
        end_tm = st.text_input("Ending time")
    else:
        start_tm,end_tm = timing.split(" - ")
    
    subject = st.selectbox("Subject code",fetch_subcode(sem))
    
    
    st.write (
        f"""
        * Semester : {sem}
        * Section : {section}
        * Day : {day}
        * Start Time : {start_tm}
        * End Time : {end_tm}
        * Subject Code : {subject}
        """
        )

    if st.button("Submit"):
        # Query to add data
        pass
        
if page_choice == pages_menu[7]:
    st.subheader("Lab Faculty Timetable")
    if(int(month) > 6):
        sem = st.selectbox("Semester",odd_sem_menu)
    else:
        sem = st.selectbox("Semester",even_sem_menu)
    section = st.text_input("Section","")
    day = st.selectbox("Day of the week to update timetable",days_of_the_week)
    timing = st.selectbox("Time Slot",time_slots)
    
    if timing == 'Other...':
        start_tm = st.text_input("Starting time")
        end_tm = st.text_input("Ending time")
    else:
        start_tm,end_tm = timing.split(" - ")
    Room = st.text_input("Room","")
    Subject = st.text_input("Subject","")

if page_choice == pages_menu[8]:
    time_slots = ["8:15 - 9:15", "9:15 - 10:15","10:45 - 11:45","11:45 - 12:45","1:30 - 2:30","3:30 - 3:45","3:45 - 4:45",'Other...']
    st.subheader("Faculty Duties")
    Initials = st.selectbox("Initials",fetch_initials())
    Duty_type = st.selectbox("Duty type",fetch_duty_type())
    Duty_duration = st.selectbox("Duration",time_slots)
    Duty_venue = st.text_input("Venue","")
    
    Duty_date = st.text_input("Date","")
    Duty_reporting_time = st.text_input("Reporting Time","")
if page_choice == pages_menu[9]:
    st.balloons()
    st.write("# Made with :heartbeat:")
    st.write("## **Abhijit Sethi**")
    st.write("## **Aditi D Anchan**")
    st.write("## **Aakanksha V Akkihal**")