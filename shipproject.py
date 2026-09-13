# Please read the commends carefully to understand the program 

#imports 
try: # Tries to import all the modules needed 
    from datetime import datetime #will be mainly used for logging
    import mysql.connector as s #will be used for everything around
    import time #will be used to program menu driven interface timings and all
    module_error_flag=False  # if no error occurs this flag will be set to false
except Exception as err:
    module_error=str(err)  # if error occurs the error will be converted into string
    module_error_flag=True  # Then the flag will be set to true 
                            # all of this is done to ensure every error is logged and thus helps in maintaince
#imports over



# function blocks for easy management

# function block for first run of program (fully hardcoded block)
 #most values here are hardcoded as to show examples and as such 
def first_run(ui_element = " "):
    log("#### program shipproject.py was started ####",escape_sequences="\n\n\n\n\n")
    def run_querie(*command):   #for error checking and handling also logs into the log.txt if the table exits 
        try: #here we check for existence of database with fact if error arises or not 
            cur1.execute(command[0])
            con1.commit()
            log("Table "+command[1]+" was not found so it was created")
            return True
        except s.errors.ProgrammingError: #here the error is used for propper logging of actions 
            log("Table "+command[1]+" already exits moving on...")
            return False

    while True:
        credentials_is_okay = False
        try:
            with open("shipproject_intialized.txt","r") as f:
                data = f.read()
                data = data.split(",")
                host_name,user_name,password_of_user = data
                f.close()
                credentials_is_okay = True
        except Exception:
            box("shipproject_intialized.txt file was not found !\n \nPlease answer the following questions carefully to setup shipproject-cli !!!",escape_sequences = ui_element, error_box = True)
            with open("shipproject_intialized.txt","w") as f:  
                host_name = input("\n" + ui_element + "Please enter host name your database server is on : ")
                user_name = input(ui_element + "Please enter the username for the database : ")
                password_of_user = input(ui_element + "Please enter the password for the database : ")
                f.write(host_name + "," + user_name + "," + password_of_user)
                f.close()
        if credentials_is_okay == True:
            break

    #con0 was oppened to intiated the check for existence of database and create it if required
    con0 = s.connect(host = host_name, user = user_name, password = password_of_user)
    cur0 = con0.cursor()
    if con0.is_connected() == True:
        log("connection 0 was connected")
    try:
        cur0.execute("create database shipproject")
        print("\n\n" + ui_element + "Database shipproject and connected tables were not found creating them please wait...")
        database_flag=0    
        log("Database shipproject was not found so it was created using connection0")
        time.sleep(1.5)  # some timing for looks 
    except s.errors.DatabaseError: # this means database was already present so it moved on 
        database_flag=1
        log("Database shipproject already exits moving on...") 
    con0.close()        #con0 was closed here 
    log("connection 0 was closed")
    global con1      #con1 is being opened here for all other interactions in this program with mysql
    con1 = s.connect(host = host_name, user = user_name, password = password_of_user,database="shipproject",)
    if con1.is_connected() == True:  
        log("connection 1 was connected")
    global cur1   # cur1 is being made into global scope for future use 
    cur1 = con1.cursor()

#login and register tables and pre-inserts some values

    #creates register_table
    run_querie("create table register_list(user_id int primary key,email_address varchar(100) not null unique,password varchar(225) not null, first_name varchar(50) not null,last_name varchar(50) not null,age int not null,phonenumber bigint unique not null,adhar_id bigint unique not null,nationality varchar(50) not null,tc char(1) not null )","register_list")
         
    #creates staff_register_table
    if run_querie("create table staff_register_list(staff_id int primary key,email_address varchar(100) not null unique,password varchar(225) not null, first_name varchar(50) not null,last_name varchar(50) not null,age int not null,phonenumber bigint unique not null,adhar_id bigint unique not null,nationality varchar(50) not null,tc char(1) not null ,is_admin char(1) not null,is_owner char(1) not null)","staff_register_list"):
        #adds admin to staff tables so admin can add the other staffs 
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(1,'ownerforshipproject@gmail.com','owner','owner for','shipproject',18,9090190901,0010,'India','y','y','y')")
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(2,'adminforshipproject@gmail.com','admin','admin for','shipproject',18,9090190991,00100,'India','y','y','n')")
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(3,'staffforshipproject@gmail.com','staff','staff for','shipproject',18,9090190999,001000,'India','y','n','n')")
        con1.commit()
        log("all basic staff entries were added to staff register list")

        # The below values are commended just for the pupose of examples and showcase this is not a security letdown
        # Also the below values are generic examples in cases of staffs and admins 
        # Admins and staff can be removed or added but owner will be hardcoded 

        # owner's staff id : 1 
        # owner's password : owner
        # admin's staff id : 2
        # admin's password : admin
        # staff's staff id : 3
        # staff's password : staff

    #creates login checklist table
    run_querie("create table login_checklist(user_id int primary key,email_address varchar(100) not null unique,phonenumber bigint not null,password varchar(225) not null)","login_checklist")

    #creates staff checklist table 
    if run_querie("create table staff_checklist(staff_id int primary key,email_address varchar(100) not null unique,phonenumber bigint not null,password varchar(225) not null,is_admin char(1),is_owner char(1))","staff_checklist"):
        #adds admin to staff tables so admin can add the other staffs
        cur1.execute("insert into staff_checklist(staff_id,email_address,phonenumber,password,is_admin,is_owner)values(1,'ownerforshipproject@gmail.com',9090190991,'owner','y','y')")
        cur1.execute("insert into staff_checklist(staff_id,email_address,phonenumber,password,is_admin,is_owner)values(2,'adminforshipproject@gmail.com',9090190901,'admin','y','n')")
        cur1.execute("insert into staff_checklist(staff_id,email_address,phonenumber,password,is_admin,is_owner)values(3,'staffforshipproject@gmail.com',9090190999,'staff','n','n')")
        con1.commit()
        log("all basic staff entries were added to staff login checklist")
        
    #creates ship history
    run_querie("create table ship_history(ship_name varchar(50),user_id int, seat_no int, allocation varchar(50), ticket_id int,food varchar(50))","ship_history")

    #creates ticket history
    run_querie("create table ticket_history(ship_name varchar(50),user_id int, ticket_id int,ticket_validity varchar(50))","ticket_history")

    #creates foodlist
    run_querie("create table foodlist(user_id int(11),ticket_id int(11),food_coupon_id int(11),food_item_name varchar(200))","foodlist")

    #creates table for ships and pre-inserts some values

    tables_to_create_list=["mv_kavaratti","pre_mv_kavaratti","mv_arabian_sea","pre_mv_arabian_sea","mv_lakshadweep_sea","pre_mv_lakshadweep_sea","mv_amindivi","pre_mv_amindivi","hsc_parali","pre_hsc_parali"]
    # the list has names of ship through which it will itrate to form the ship tables

    for table_name_index in range(0,len(tables_to_create_list)):
        table_to_create=tables_to_create_list[table_name_index]
        if run_querie("create table "+table_to_create+"(ship_name varchar(50), user_id int, seat_no int, allocation varchar(50), ticket_id int,ticket_validity varchar(50),food varchar(50))",table_to_create):
            for seat_no in range(1,51):
                seat_no_str=str(seat_no)
                cur1.execute("insert into "+table_to_create+"(ship_name,seat_no,allocation,ticket_validity,food)values('"+table_to_create+"','"+seat_no_str+"','disallocated','Not booked','not booked')")
                con1.commit()
            log("all basic values were inserted into "+table_to_create)

    if database_flag==0: #this is database flag from con0 side which shows the confirmation (check con0 for reference)
        print("\n" + ui_element + "Done !")
        time.sleep(1) # some timing for looks 
        print("\n"*100) #prints 100 newlines in intention to clear terminal
#block end


# fuction block for user regiasteration (part 1)
def user_registeration(ui_element):
    cur1.execute("select max(user_id) from register_list")  #selects the biggest user od or the last registered user id from table 
    data = cur1.fetchall() # just stores the last regisered user id 
    if data[0][0] == None:
        user_id = 0 # if no user id was found meaning the database was just created it sets default to 0
    else:
        user_id = data[0][0] + 1
    data_list_to_collect = ["email_address","password","first name","last name","age","phonenumber","adhar_id","nationality","tc"]
    print()
    values_1 = data_catching(data_list_to_collect,ui_element)  #this function will catch all the data here
    values_1.insert(0,user_id)
    values_2 = (values_1[0],values_1[1],values_1[6],values_1[2])

    try:
        cur1.execute("insert into register_list(user_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values_1)
        cur1.execute("insert into login_checklist(user_id,email_address,phonenumber,password)values(%s,%s,%s,%s)",values_2)
        box("!!! succesfully registered !!!\n \nPlease remember your User ID and password !\nYour User is : " + str(user_id) +"\nYour password is : " + values_2[3],escape_sequences = ui_element, error_box = True )
        log("a user was registered with user id : " + str(user_id))
        con1.commit()
    except s.errors.IntegrityError:
        box("Registration failed !\nPlease enter your own email, phonenumber, adhar ID and check for its correctness",escape_sequences = ui_element, warning_box = True)
        log("registration failed, user entred wrong email,phonenumber etc")
#block end

# fuction block for staff registeration1
def staff_registeration(ui_element,privilage_level,staff_type_to_add):
    cur1.execute("select max(staff_id) from staff_register_list")  #selects the biggest staff id or the last registered staff id from table 
    data = cur1.fetchall() # just stores the last registered staff id
    if data[0][0] == None:
        staff_id = 0 # if no staff id was found meaning the database was just created it sets default to 0
    else:
        staff_id = data[0][0] + 1

    if privilage_level == "admin" and staff_type_to_add == "staff":
        is_admin="n"
        is_owner="n"
    elif privilage_level == "owner" and staff_type_to_add == "staff":
        is_admin="n"
        is_owner="n"
    elif privilage_level == "owner" and staff_type_to_add == "admin":
        is_admin="y"
        is_owner="n"

    data_list_to_collect = ["email_address","password","first name","last name","age","phonenumber","adhar_id","nationality","tc"]
    print()
    values_1 = data_catching(data_list_to_collect,ui_element)  #this function will catch all the data here
    values_1.insert(0,staff_id)
    values_1.append(is_admin)
    values_1.append(is_owner)
    values_2 = (values_1[0],values_1[1],values_1[6],values_1[2],is_admin,is_owner)

    try:
        cur1.execute("insert into staff_register_list(staff_id,email_address,password,first_name,last_name,age,phonenumber,adhar_id,nationality,tc,is_admin,is_owner)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",values_1)
        cur1.execute("insert into staff_checklist(staff_id,email_address,phonenumber,password,is_admin,is_owner)values(%s,%s,%s,%s,%s,%s)",values_2)
        box("!!! succesfully registered !!!\n \nPlease remember your User ID and password !\nYour User is : " + str(staff_id) +"\nYour password is : " + values_2[3],escape_sequences = ui_element, error_box = True )
        log("a staff was registered with staff id : " + str(staff_id))
        con1.commit()
    except s.errors.IntegrityError:
        box("Registration failed !\nPlease enter your own email, phonenumber, adhar ID and check for its correctness",escape_sequences = ui_element, warning_box = True)
        log("registraion failed, staff entred wrong email,phonenumber etc")


#function block for staff login
def staff_login(ui_element):
    for tries in range(3):  #just means you have three tries
        staff_id = input("\n" + ui_element + "Please enter you staff id :") #picks up staff id 
        try:
            if staff_id.isdigit() == False: #checks if its digit
                box("Please enter proper staff ID", escape_sequences = ui_element, warning_box = True) 
                log("login failed staff_id " + staff_id + "was inappropriate")
                continue
            password_entered_by_staff=input(ui_element + "Please enter your pasasword :")
            cur1.execute("select password from staff_checklist where staff_id = %s",(staff_id,))
            data = cur1.fetchall()  #retirves password from database matching to staff id
            password_in_databse = data[0][0]
            if password_in_databse == password_entered_by_staff:    #checks if both are same
                cur1.execute("select is_owner from staff_checklist where staff_id = %s",(staff_id,))
                is_owner = cur1.fetchall()   #retirves owner status "y" or "n"
                if is_owner[0][0] == "y":    #if owner return "logged_in-owner",staff_id
                    log("staff logged as owner with staff_id : " + staff_id)
                    print(ui_element + "logged in as owner !")
                    return "logged_in-owner",staff_id
                cur1.execute("select is_admin from staff_checklist where staff_id = %s",(staff_id,))
                is_admin = cur1.fetchall()  #same like owner
                if is_admin[0][0] == "y":   #same like owner
                    log("staff logged as admin with staff_id : " + staff_id)
                    print(ui_element + "logged in as admin !")
                    return "logged_in-admin",staff_id
                else:   #if it was not admin or owner they are normal staff so they will be logged in like that 
                    log("staff logged as staff with staff_id : " + staff_id)
                    print(ui_element + "logged in as staff !")
                    return "logged_in-staff",staff_id
            else:
                log("login failed with staff id " + staff_id + " beacuse passwords did not match")  # both passwords didnt match this executes
                box("Either staff_id or password was wrong please retry", escape_sequences = ui_element, warning_box = True)
                continue
        except IndexError:  #this occurs when password for the certain staff id was not found in database
            box("Either staff_id or password was wrong please retry", escape_sequences = ui_element, warning_box = True)
            log("login failed beacuse no staff with that passsoword was found")
            continue
    box("Login failed you have used all three tries", escape_sequences = ui_element, warning_box = True)
    log("login failed due to user error")
    return "login_failed",None   #if all atempts failed lgin fails
#end block


#function block for login 
def login(ui_element):
    for tries in range(3):  #just means you have three atempts at login
        user_id = input("\n" + ui_element + "Please enter you user id :") #picks up user id 
        try:
            if user_id.isdigit() == False:      #checks user if if its valid
                box("Please enter proper user ID", escape_sequences = ui_element, warning_box = True)                     
                log("login failed user id " + user_id + " was inappropriate")
                continue
            password_entered_by_user = input(ui_element + "Please enter your password :")
            cur1.execute("select password from login_checklist where user_id = %s",(user_id,))
            data = cur1.fetchall() # fetchs password for comparing
            password_in_database = data[0][0] # extracts password for comparing cause it in form [(passwd,),]
            if password_in_database == password_entered_by_user:
                log("user succesfully loged in with user id : " + user_id)
                print("\n" + ui_element + "login succesfull !")
                return "logged_in-user",user_id
            else:
                log("login failed user with user id " + user_id + "because passwords did not match")
                box("Either user_id or password was wrong please retry", escape_sequences = ui_element, warning_box = True)
                continue
        except IndexError:  #this occurs when password for the certain user id was not found in database
            box("Either user_id or password was wrong please retry", escape_sequences = ui_element, warning_box = True)
            log("login failed becuase no user with that password was found")
            continue
    box("Login failed you have used all three tries", escape_sequences = ui_element, warning_box = True)
    log("login failed due to user error")
    return "login_failed",None
#end block

#function for database console 
def database_console(ui_element,console_user):
    if console_user == "admin":
        console_con = con1
        console_cur = cur1
    if console_user == "owner":
        console_con = con1
        console_cur = cur1
    box("Please use console with atmost care !\n \nElse things can get corrupted !\n \nPlease enter queries without ';'", escape_sequences = ui_element, error_box = True)
    while True:
        box("1.Pure Querie\n2.Querie With Value Fetching\n3.Exit Console", escape_sequences = ui_element, menu = True)
        opt = data_catching(["option",],ui_element,option_range = (1,3))
        if opt == 1:
            querie = input("\n" + ui_element + "Please enter querie : ")
            try:
                console_cur.execute(querie)
                console_con.commit()
                print("\n" + ui_element + "Querie executed successfully !")
            except Exception:
                box("Querie Errored Out !!!", escape_sequences = ui_element, warning_box = True)
        if opt == 2:
            querie = input("\n" + ui_element + "Please enter querie : ")
            try:
                console_cur.execute(querie)
                data = console_cur.fetchall()
                print("\n" + ui_element + "Querie executed successfully !")
                print("\n" + ui_element + "Results : ")

                if data == []:
                    box("There is no result to show", escape_sequences = ui_element, warning_box = True)
                elif data == [()]:
                    box("There is no result to show", escape_sequences = ui_element, warning_box = True)
                else:
                    box(data, escape_sequences = ui_element)
            except Exception:
                box("Querie Errored Out !!!", escape_sequences = ui_element, warning_box = True)
        if opt == 3:
            return None


#fucntion block for staff removal
def remove_staff(ui_element,privilage_level,staff_type_to_remove):

    def authority_checker(staff_feild_name):
        cur1.execute("select " + staff_feild_name + " from staff_checklist where staff_id=%s",(staff_id,))
        try:
            authority_check = cur1.fetchall()[0][0]
            return authority_check
        except Exception as err:
            print(err)
            box("Staff with that staff ID does not exist !", escape_sequences = ui_element, warning_box = True)
            return None

    staff_id = data_catching(["number",],ui_element,custom_message = "Please enter the staff id of staff which you want to delete : ")
    choice_confirmation = data_catching(["yes or no",],ui_element,custom_message = "Do you want to continue (y/n) : ")

    if choice_confirmation in ["n","N",None]:
        return None

    elif privilage_level == "owner" and staff_type_to_remove == "admin" or staff_type_to_remove == "staff":
        authority_check = authority_checker("is_owner")
        if authority_check == None: #just goes back if staff with that id didnt exist 
            return None
        if authority_check == "y":  #this would mean owner was trying to reomve himself
            box("you dont have permission to remove yourself !", escape_sequences = ui_element, warning_box = True)
            return None
        authority_check = authority_checker("is_admin")
        if authority_check == None: #just goes back if staff with that id didnt exist
            return None
        if authority_check == "n" and staff_type_to_remove == "admin":    #this would mean owner tried to remove staff with admin removal feature
            box("This feature is for only removal of admins !\nPlease use staff removal feature for that", escape_sequences = ui_element, warning_box = True)
            return None
        if authority_check == "y" and staff_type_to_remove == "staff":    #this would mean owner tried to use staff removal feature for admin removal 
            box("This part of menu is meant to remove normal staffs\nPlease use admin removal part of menu", escape_sequences = ui_element, warning_box = True)
            return None
        #if it passed all cretierieas and error checks staff is deleted
        cur1.execute("delete from staff_checklist where staff_id=%s",(staff_id,))
        cur1.execute("delete from staff_register_list where staff_id=%s",(staff_id,))
        con1.commit()
        log(staff_type_to_remove + " with staff ID, " + str(staff_id) + " was removed by owner")
        print("\n" + ui_element + staff_type_to_remove + " with staff ID, " + str(staff_id) + " was removed successfully !")
    elif privilage_level == "admin" and staff_type_to_remove == "staff":
        authority_check = authority_checker("is_owner")
        if authority_check == None: #just goes back if staff with that id didnt exist
            return None
        if authority_check == "y":
            box("you dont have permission to remove owner !", escape_sequences = ui_element, warning_box = True)
            return None
        authority_check = authority_checker("is_admin")
        if authority_check == None: #just goes back if staff with that id didnt exist
            return None
        if authority_check == "y":
            box("you dont have permission to remove another admin or yourself !", escape_sequences = ui_element, warning_box = True)
            return None
        #if it passed all cretierieas and error checks staff is deleted
        cur1.execute("delete from staff_checklist where staff_id=%s",(staff_id,))
        cur1.execute("delete from staff_register_list where staff_id=%s",(staff_id,))
        con1.commit()
        log(staff_type_to_remove + " with staff ID, " + str(staff_id) + " was removed by owner")
        print("\n" + ui_element + staff_type_to_remove + " with staff ID, " + str(staff_id) + " was removed successfully !")
#block end 

#function block for booking ticket
def book_ticket(user_id,ui_element,booking_type="booking"):
    box("1.MV Kavaratti ( Kochi --> Kavaratti )\n2.MV Arabian Sea ( Kochi --> Minicoy )\n3.MV Lakshadweep Sea ( Kochi --> Kalpeni )\n4.MV Amindivi ( Beypore --> Amini )\n5.HSC Parali ( Kochi --> Agatti )\n6.Go back to previous menu", escape_sequences = ui_element, menu = True)   #just prints meanu in a box
    opt = data_catching(["option"],ui_element, option_range = (1,6)) # takes in a option 
    if opt == None:
        return "booking_failed"
    payment_check=input("\n" + ui_element + "Have you have completed your payment at counter (y/n) : ")
    def book(ship_name,user_id):
        cur1.execute("select min(seat_no) from " + ship_name + " where allocation='disallocated'")
        data = cur1.fetchall()
        seat_no = data[0][0]
        cur1.execute("select max(ticket_id) from ticket_history")
        data = cur1.fetchall()
        ticket_id = data[0][0]
        if seat_no == None and booking_type == "prebooking":
            box("Sorry to dissapoint you but all seats are booked !\nPlease try another day !",escape_sequences = ui_element, warning_box = True)
            log("booking failed due to full seats")
            return "booking_failed"
        elif seat_no == None:
            box("Sorry to dissapoint you but all seats are booked !\nPlease use the pre-booking area for travelling another day !", escape_sequences = ui_element, warning_box = True)
            log("booking failed due to full seats")
            return "booking_failed"
        if ticket_id == None:
            cur1.execute("insert into ticket_history(ship_name,user_id,ticket_id,ticket_validity)values(%s,%s,1,'valid')",(ship_name,user_id))
            cur1.execute("update " + ship_name + " set user_id=%s,ticket_id=1,ticket_validity='valid',allocation='allocated' where seat_no=%s",(user_id,seat_no))
            con1.commit()
            print("\n" + ui_element + "Ticket was booked succesfully")
            log("Ticket was booked succesfully")
        else:
            ticket_id = ticket_id + 1
            cur1.execute("insert into ticket_history(ship_name,user_id,ticket_id,ticket_validity)values(%s,%s,%s,'valid')",(ship_name,user_id,ticket_id))
            cur1.execute("update " + ship_name + " set user_id=%s,ticket_id=%s,ticket_validity='valid',allocation='allocated' where seat_no=%s",(user_id,ticket_id,seat_no))
            con1.commit()
            print("\n" + ui_element + "Ticket was booked succesfully")
            log("Ticket was booked succesfully")

    #for prebooking
    if payment_check in ["y","Y"] and booking_type=="prebooking":
        if opt == 1:
            book("pre_mv_kavaratti",user_id)
            return "booked_ticket"
        if opt == 2:
            book("pre_mv_arabian_sea",user_id)
            return "booked_ticket"
        if opt == 3:
            book("pre_mv_lakshadweep_sea",user_id)
            return "booked_ticket"
        if opt == 4:
            book("pre_mv_amindivi",user_id)
            return "booked_ticket"
        if opt == 5:
            book("pre_hsc_parali",user_id)
            return "booked_ticket"

    #for normal booking 
    elif payment_check in ["y","Y"] and booking_type=="booking":
        if opt == 1:
            book("mv_kavaratti",user_id)
            return "booked_ticket"
        if opt == 2:
            book("mv_arabian_sea",user_id)
            return "booked_ticket"
        if opt == 3:
            book("mv_lakshadweep_sea",user_id)
            return "booked_ticket"
        if opt == 4:
            book("mv_amindivi",user_id)
            return "booked_ticket"
        if opt == 5:
            book("hsc_parali",user_id)
            return "booked_ticket"

    elif payment_check in ["n","N"]:
        box("Please complete payment at counter !",escape_sequences = ui_element,warning_box = True)
        log("booking failed due to payment issues")
        return "booking_failed"
    else:
        box("Please enter an appropriate option",escape_sequences = ui_element,warning_box = True)
        log("booking failed due to user error")
        return "booking_failed"

#block end

#fucntion block for seeing info regarding diffrent matters
def see_info(ui_element,info_type):
    def select_ship(ship_type="normal"):
        if ship_type=="pre":
            box("1.Pre-MV Kavaratti\n2.Pre-Mv Arabian Sea\n3.Pre-Mv Lakshadweep Sea\n4.Pre-Mv Amindivi\n5.Pre-HSC Parali\n6.Go Back",escape_sequences = ui_element, menu = True)
            opt = data_catching(["option",], ui_element, option_range = (1,6))
            if opt == 1:
                return "pre_mv_kavaratti"
            if opt == 2:
                return "pre_mv_arabian_sea"
            if opt == 3:
                return "pre_mv_lakshadweep_sea"
            if opt == 4:
                return "pre_mv_amindivi"
            if opt == 5:
                return "pre_hsc_parali"
            if opt == 6:
                return  None
            if opt == None:
                return None
        if ship_type=="normal":
            box("1.MV Kavaratti\n2.Mv Arabian Sea\n3.Mv Lakshadweep Sea\n4.Mv Amindivi\n5.HSC Parali\n6.Go Back",escape_sequences = ui_element, menu = True)
            opt = data_catching(["option",], ui_element, option_range = (1,6))
            if opt == 1:
                return "mv_kavaratti"
            if opt == 2:
                return "mv_arabian_sea"
            if opt == 3:
                return "mv_lakshadweep_sea"
            if opt == 4:
                return "mv_amindivi"
            if opt == 5:
                return "hsc_parali"
            if opt == 6:
                return None
            if opt == None:
                return None

    if info_type == "ship info-current":
        ship_name = select_ship()
        if ship_name == None:
            return None
        cur1.execute("select * from " + ship_name)
        info = cur1.fetchall()
        if info != []:
            box(info,table_name = ship_name, escape_sequences = ui_element)
        else:
            box("Table is empty !",escape_sequences = ui_element, warning_box = True)
    if info_type == "ship info-prebooking":
        ship_name = select_ship(ship_type="pre")
        if ship_name == None:
            return None
        cur1.execute("select * from " + ship_name)
        info = cur1.fetchall()
        if info != []:
            box(info,table_name = ship_name, escape_sequences = ui_element)
        else:
            box("Table is empty !",escape_sequences = ui_element, warning_box = True)
    if info_type == "ship history":
        cur1.execute("select * from ship_history")
        info = cur1.fetchall()
        if info != []:
            box(info,table_name="ship_history",escape_sequences = ui_element)
        else:
            box("Table is empty !",escape_sequences = ui_element, warning_box = True)
    if info_type == "ticket history":
        cur1.execute("select * from ticket_history")
        info = cur1.fetchall()
        if info != []:
            box(info,table_name = "ticket_history", escape_sequences = ui_element)
        else:
            box("Table is empty !",escape_sequences = ui_element, warning_box = True)
#end of block


#function block for deactivating and updating tickets
def update_ticket(ui_element,user_type,update_type="deactivate"):
    ticket_id = data_catching(["ticket id",],ui_element)

    def show_info_on_ticket_id(ticket_id):
        cur1.execute("select ship_name from ticket_history where ticket_id=%s and ticket_validity='valid'",(ticket_id,))
        data = cur1.fetchall()
        if data == []:
            box("A Ticket Like that does not exist which is valid\nCancelling Updataion of Ticket", escape_sequences = ui_element, warning_box = True)
            log("Ticket with Ticket ID " + str(ticket_id) + " was not found process cancelled")
            return False,False
        ship_name = data[0][0]
        cur1.execute("select * from ticket_history where ticket_id=%s and ticket_validity='valid'",(ticket_id,))
        ticket_info1 = cur1.fetchall()
        cur1.execute("select * from " + ship_name + " where ticket_id=%s  and ticket_validity='valid'",(ticket_id,))
        ticket_info2 = cur1.fetchall()
        if ticket_info1 == [] or ticket_info2 == [] or data == []:
            box("A Ticket Like that does not exist which is valid\nCancelling Updataion of Ticket", escape_sequences = ui_element, warning_box = True)
            log("Ticket with Ticket ID " + str(ticket_id) + " was not found process cancelled")
            return False,False
        box(ticket_info1, table_name = "ticket_history", escape_sequences = ui_element)
        box(ticket_info2, table_name = ship_name, escape_sequences = ui_element)
        return True, ship_name
    
    if update_type == "deactivate":
        ticket_id_is_valid, ship_name = show_info_on_ticket_id(ticket_id)
        if ticket_id_is_valid == False:
            return None
        confirmation=input("\n" + ui_element +"The ticket would be registered deactivated on both these tables, do you want to continue (y/n) : ")
        if confirmation in ["y","Y"]:
            cur1.execute("update ticket_history set ticket_validity='deactivated' where ticket_id=%s",(ticket_id,))
            cur1.execute("update " + ship_name + " set ticket_validity='deactivated',allocation='disallocated',food='not booked' where ticket_id=%s",(ticket_id,))
            con1.commit()
            print("\n" + ui_element + "changes were made !")
            log("Ticket with Ticket ID " + str(ticket_id) + " was deactivated")
        else:
            print("\n" + ui_element + "proccess cancelled !")
            log("Updation of Ticket was cancelled by " + user_type)
            return None

    if update_type=="refund":
        ticket_id_is_valid, ship_name = show_info_on_ticket_id(ticket_id)
        if ticket_id_is_valid == False:
            return None
        confirmation=input("\n\t\tThe ticket would be registered refunded on both these tables, do you want to continue (y/n) : ")
        if confirmation in ["y","Y"]:
            cur1.execute("update ticket_history set ticket_validity='refunded' where ticket_id=%s",(ticket_id,))
            cur1.execute("update "+ship_name+" set ticket_validity='refunded',allocation='disallocated',food='not booked' where ticket_id=%s",(ticket_id,))
            con1.commit()
            print("\n" + ui_element + "changes were made !")
            log("Ticket with Ticket ID " + str(ticket_id) + " was refunded")
        else:
            print("\n" + ui_element + "proccess cancelled !")
            log("Updation of Ticket was cancelled by " + user_type)
            return None
#block end

#fucntion block for seeing tickets booked by specific user who logged in 
def see_tickets_for_user(user_id,ui_element):
    while True:
        box("1.Active Tickets\n2.Refunded Tickets\n3.Inactive Tickets\n4.Go Back",escape_sequences = ui_element, menu = True)
        opt = data_catching(["option",],ui_element, option_range = (1,4))
        if opt == 1:
            ship_namelist_to_scan=["mv_kavaratti","pre_mv_kavaratti","mv_arabian_sea","pre_mv_arabian_sea","mv_lakshadweep_sea","pre_mv_lakshadweep_sea","mv_amindivi","pre_mv_amindivi","hsc_parali","pre_hsc_parali"]

            final_list_of_active_tickets=[]

            for ship_name in ship_namelist_to_scan:
                cur1.execute("select * from " + ship_name + " where user_id=" + user_id + " and ticket_validity='valid'")
                data = cur1.fetchall()
                for row in data:
                    final_list_of_active_tickets.append(row)
            if final_list_of_active_tickets == []:
                box("You have 0 active tickets booked", escape_sequences = ui_element, warning_box = True)
                continue
            box(final_list_of_active_tickets, table_name = "mv_kavaratti", escape_sequences = ui_element)
            log("user viewed all his active tickets")
            continue
        if opt == 2:
            cur1.execute("select * from ticket_history where user_id=" + user_id + " and ticket_validity='refunded'")
            refunded_tickets = cur1.fetchall()
            if refunded_tickets == []:
                box("You have 0 refunded tickets", escape_sequences = ui_element, warning_box = True)
                continue
            box(refunded_tickets,table_name="ticket_history", escape_sequences = ui_element)
            log("user viewed all his refunded tickets")
        if opt == 3:
            cur1.execute("select * from ticket_history where user_id=" + user_id + " and ticket_validity='deactivated'")
            deactivated_tickets = cur1.fetchall()
            if deactivated_tickets == []:
                box("You have 0 deactivated tickets", escape_sequences = ui_element, warning_box = True)
                continue
            box(deactivated_tickets,table_name = "ticket_history",escape_sequences = ui_element)
            log("user viewed all his deactivated tickets")
        if opt == 4:
            return None
#block end

#function block for booking food 
def book_food(user_id, ui_element):
    ticket_id = data_catching(["ticket id",],ui_element)

    food_list=["Rotti and Beef chops","Dosa and Curries","Lemon rice","Biriyani","Idli and Curries","Meals","Al-faham","Fried rice and Chilli gopi or Chilli chicken","Chole batture","Aloo paratha","Butter garlic naan and palak paneer","Chicken noodles","Mushroom soup","Vada pav","Omelette","Fish fry","Samosa and Chuttney","Popcorn","Burger (type choosable at food stall)","Pizza (type choosable at food stall)","Mango lassi","Soda items (can be selected from food stall)","Tea/Coffe (can be selectd from food stall)","Fresh lime","Water"]

    box(food_list,escape_sequences = ui_element, list_only = True, numbered = True)
   
    food_selection = data_catching(["option",],ui_element,option_range = (1,25))
    food_selection -= 1
    payment_check=input("\n" + ui_element + "Did you complete the payment at the counter (y/n) : ")
    food_item_name = food_list[food_selection]

    if payment_check in ["Y","y"]:
        cur1.execute("select max(food_coupon_id) from foodlist")
        food_coupon_id = cur1.fetchall()
        food_coupon_id = food_coupon_id[0][0]
        if food_coupon_id == None:
            food_coupon_id=0
        else:
            food_coupon_id += 1
        try:
            values = (user_id,ticket_id,food_coupon_id,food_item_name)
            cur1.execute("insert into foodlist(user_id,ticket_id,food_coupon_id,food_item_name)values(%s,%s,%s,%s)",values)
            con1.commit()

            ship_namelist_to_scan_and_update = ["mv_kavaratti","pre_mv_kavaratti","mv_arabian_sea","pre_mv_arabian_sea","mv_lakshadweep_sea","pre_mv_lakshadweep_sea","mv_amindivi","pre_mv_amindivi","hsc_parali","pre_hsc_parali"]

            try:
                for ship_name in ship_namelist_to_scan_and_update:
                    cur1.execute("update " + ship_name + " set food = 'booked' where ticket_id=%s",(ticket_id,))
            except Exception:
                pass

            print("\n" +  ui_element + food_item_name + " was succesfully booked !")
            log("food was booked for the user succesfully")
        except Exception:
            box("Please enter a valid Ticket ID", escape_sequences = ui_element, error_box = True)
            log("food booking failed due invalid Ticket ID")
            return None
    else:
        box("Please complete the payment at counter !", escape_sequences = ui_element, warning_box = True)
        log("food booking faied due to payment issues")
#block end

#function block for checking of emails and passwords as such since i dont wanna repeat it nor huge pain reading stuff 
def data_catching(typelist,ui_element,option_range = None,custom_message= "None",usecase = None):
    
    data_list = []      #we add data to return in the end to its
                        #if all went fine the data will be returned as list containing everything requested
    #Functions are defined here so that they not need to get redefined everytime when for loop runs 
    def name_validation(name_to_validate): #this function will be used later for name validation
        char_is_valid = True
        for char in name_to_validate:
            if char.isspace():
                box(type + " cannot contain spaces",escape_sequences = ui_element,warning_box = True)
                char_is_valid = False 
            elif char.isdigit():
                box(type + " cannot contain numbers",escape_sequences = ui_element,warning_box = True)
                char_is_valid = False
            elif char.isalpha() == False:
                box(type + " cannot contain special charecters",escape_sequences = ui_element,warning_box = True)
                char_is_valid = False
        if char_is_valid == False:
            return  None
        else:
            return name_to_validate

    def email_local_part_validation():      #validation of the local part 
        special_chars = "._-+"      #speical chars which are allowed in email address
        if len(local_part) > 64:    #local part checking starts
            box("part before \"@\" must be less than or equal to 64 charecters",escape_sequences = ui_element,warning_box = True)
            return None
        elif len(local_part) < 1:
            box("Part before \"@\" must be more than or equal to 1 charecter",escape_sequences = ui_element,warning_box= True)
            return None
        if local_part[0].isalnum() == False or local_part[len(local_part) - 1].isalnum() == False:
            box("Part before \"@\" must start and end with alpha-numeric charecters",escape_sequences = ui_element,warning_box = True)
            return None
        for i in range(len(local_part)):
            if i == len(local_part) - 1:
                pass
            elif local_part[i] in special_chars and local_part[i + 1] in special_chars:
                box("\".\" ,\"_\" ,\"-\" ,\"+\" cannot be used consiqutively",escape_sequences = ui_element,warning_box = True)
                return None
            if local_part[i] not in special_chars and local_part[i].isalnum() == False:
                box("Charecters other than \".\" ,\"_\" ,\"-\" ,\"+\" cannot be used in email",escape_sequences = ui_element,warning_box = True) 
                return None
        return local_part

    def email_domain_validation():  #validation of domain
        special_chars = ".-"
        if domain.count(".") < 1:
            box("A domain must contain at least one \".\"",escape_sequences = ui_element,warning_box = True)
            return None
        if len(domain) < 4 or len(domain) > 255:
            box("A domain should be between 4 and 255 charecters long",escape_sequences = ui_element,warning_box = True)
            return None
        if domain[0].isalnum() == False or domain[len(domain) - 1].isalnum() == False:
            box("A domain cannot start or end with special charecters",escape_sequences = ui_element,warning_box = True)
            return None
        for i in range(len(domain)):
            if i == len(domain) - 1:
                pass
            elif domain[i] + domain[i + 1] in ["..",".-","-."]:
                box("A domain cannot have \".\", \"-\" used consiqutivel",escape_sequences = ui_element,warning_box = True)
                return None
            if domain[i] not in special_chars and domain[i].isalnum() == False:
                box("A domain cannot have special charecters other than \".\", \"-\"",escape_sequences = ui_element,warning_box = True)
                return None
        label_list = domain.split(".")
        for label in range(len(label_list)):
            if label == len(label_list) - 1:      #to check if it was final domain
                if len(label_list[label]) < 2 or len(label_list[label]) > 63:
                    box("The final label in a domain should be between 2 and 63 charcters long",escape_sequences = ui_element,warning_box = True)
                    return None
                if label_list[label].isalpha() == False:
                    box("The final label in a domain should only contain alphabets",escape_sequences = ui_element,warning_box = True)
                    return None
            elif len(label_list[label]) < 1 or len(label_list[label]) > 63:
                box("The labels should between 1 and 64 charecters long",escape_sequences = ui_element,warning_box = True)
                return None
        return domain


    #a list containing values to return get passed or so called a typelist by me 
    for type in typelist:
        #we itrate through the typelist to featch all the values neccesary
        all_tries_failed = True #this is set as a default value beacause if any one attempt for the value we are catching-
                                # -and validating doesn't succed it will cause user to redo what they were doing
        if type == "email_address":
            for s in range(3):
                error_flag = 0
                email = input(ui_element + "Please enter a valid email address : ")

                if len(email) > 320 or len(email) < 6:        #global checking for errors
                    box("An email cannot have more than 320 charecters or less than 6 charecters",escape_sequences = ui_element,error_box = True)
                    error_flag = 1
                if " " in email:
                    box("An email cannot contain whitespaces", escape_sequences = ui_element, error_box = True)
                    error_flag = 1
                if email.count("@") != 1:
                    box("An email must contain one \"@\" symbol, not more not less",escape_sequences = ui_element,error_box = True)
                    error_flag = 1 

                if error_flag != 1:       #spliting local part of email and domain for seprate validation
                    local_part,domain = email.split("@")    #splitting only happens if its free from global errors
                    
                    if local_part == "" or domain == "":        #if any of parts are missing
                        box("There should be a part before and after the \"@\" symbol",escape_sequences = ui_element,error_box =True)
                    else:   #if parts are not missing it enters else block
                        checked_local_part = email_local_part_validation()
                        checked_domain = email_domain_validation()
                        if checked_local_part == None or checked_domain == None:
                            pass  #that would mean it spotted error in email in above functions
                        else:
                            data_list.append(checked_local_part + "@" + checked_domain)
                            all_tries_failed = False
                            break
                            #if it reached here it means the email was fully valid 
                
            if all_tries_failed == True:
               return None #returning none means the user will have to retry what ever usecase he was in

        elif type == "password":    #basic password verification
            for i in range(3):      
                password_first_try = input(ui_element + "Please enter a password :") #reading password for first time
                
                password_is_false = False
                if len(password_first_try) < 8: #basic validation starts here
                    box("The password should be at least 8 charecters",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True
                elif len(password_first_try) > 50:
                    box("The password should not be more than 50 charecters",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True
                contains_uppercase = False
                contains_lowercase = False
                contains_special_chars = False
                contains_numbers = False
                for i in password_first_try:
                    if contains_uppercase == False and i.isupper() == True:
                        contains_uppercase = True
                    if contains_lowercase == False and i.islower() == True:
                        contains_lowercase = True
                    if contains_numbers == False and i in "1234567890":
                        contains_numbers = True
                    if contains_special_chars == False and i.isalnum() == False:
                        contains_special_chars = True
                if contains_uppercase == False:
                    box("Password should contain at least one uppercase letter",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True
                if contains_lowercase == False:
                    box("Password should contain at least one lowercase letter",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True
                if contains_numbers == False:
                    box("Password should contain at least one number",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True
                if contains_special_chars == False:
                    box("Password should contain at least one special charecter",escape_sequences = ui_element,warning_box = True)
                    password_is_false = True

                password_final_try = input(ui_element + "Please enter your password again for confirmation :")
                #reading password for second time
                if password_is_false == True:
                    box("Password is invalid please retry",escape_sequences = ui_element,error_box = True)
                elif password_first_try != password_final_try: #checking if both passwords are same 
                    box("Both passwords were not the same please try again",escape_sequences = ui_element,error_box = True)
                else:
                    data_list.append(password_final_try)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None #it would make the user redo the whole thing again if they make three atempts wrong
        
        elif type == "first name" or type == "nationality": 
            #same system can be used for nationality or other things which is a name you just need to modify bit
            for i in range(3):
                first_name = input(ui_element + "Please enter your " + type + " : ")
                first_name = name_validation(first_name)
                if type == "nationality":
                    middle_name_confirmation = "n"
                else:
                    middle_name_confirmation = input("\n" + ui_element + "Do you have a middle name ? (y/n)")
                if middle_name_confirmation not in ["y","Y","n","N"]:
                    box("Inavalid choice please enter valid choice",escape_sequences = ui_element,warning_box = True)
                elif middle_name_confirmation in ["y","Y"]:
                    print("\n" + ui_element + "Your middle name will be added along with first name in appropriate manner")
                    middle_name = input("\n" + ui_element + "Please enter your middle name : ")
                    middle_name = name_validation(middle_name)
                else:
                    middle_name = None

                if middle_name_confirmation in ["n","N"] and first_name != None:
                    data_list.append(first_name)
                    all_tries_failed = False
                    break
                elif first_name != None and middle_name != None:
                    first_name = first_name + " " + middle_name
                    data_list.append(first_name)
                    all_tries_failed = False
                    break

            if all_tries_failed == True:
                return None

        elif type == "last name":
            for i in range(3):
                last_name = input(ui_element + "Please enter your last name : ")
                last_name = name_validation(last_name)
                if last_name != None:
                    data_list.append(last_name)
                    all_tries_failed = False
                    break

            if all_tries_failed == True:
                return None

        elif type == "phonenumber": #basic phonenumber validation we assume its india
            for i in range(3):
                phonenumber_is_valid = True
                phonenumber = input(ui_element + "Please enter your phonenumber : ")
                if phonenumber.isdigit() == False:
                    box("Phonenumber cannot have any other charecters than numbers",escape_sequences = ui_element,warning_box = True)
                    phonenumber_is_valid = False
                if len(phonenumber) > 10 or len(phonenumber) < 10:
                    box("Phonenumber should be exactly 10 numbers long",escape_sequences = ui_element,warning_box = True)
                    phonenumber_is_valid = False
                if phonenumber_is_valid == True:
                    data_list.append(phonenumber)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None
                
        elif type == "adhar_id":
            for i in range(3):
                adhar_id_is_valid = True
                adhar_id = input(ui_element + "Please enter your adhar ID : ")
                if adhar_id.isdigit() == False:
                    box("Adhar ID cannot have any other charecters than numbers",escape_sequences = ui_element,warning_box = True)
                    adhar_id_is_valid = False
                if len(adhar_id) > 12 or len(adhar_id) < 12:
                    box("Adhar ID should be exactly 12 numbers long",escape_sequences = ui_element,warning_box = True)
                    adhar_id_is_valid = False
                if adhar_id_is_valid == True:
                    data_list.append(adhar_id)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None

        elif type == "age":
            for i in range(3):
                age_is_valid = True
                age = input(ui_element + "Please enter you age : ")
                if age.isdigit() == False:
                    box("Age should not have any charecters than number",escape_sequences = ui_element,warning_box = True)
                    age_is_valid = False
                if int(age) < 0:
                    box("age cannot be less than 0",escape_sequences = ui_element,warning_box = True)
                    age_is_valid = False
                if int(age) > 120:
                    box("Age cannot be more than 120",escape_sequences = ui_element,warning_box = True)
                    age_is_valid = False
                if age_is_valid == True:
                    data_list.append(age)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None

        elif type == "ticket id" or type == "number":
            for i in range(3):
                number_is_valid = True
                if type == "ticket id":
                    number = input(ui_element + "Please enter your ticket id : ")
                else:
                    number = input(ui_element + custom_message)
                if number.isdigit() == False:
                    box(type + " should not have any charecters than number",escape_sequences = ui_element,warning_box = True)
                    number_is_valid = False
                if int(number) < 0:
                    box(type + " cannot be less than 0",escape_sequences = ui_element,warning_box = True)
                    number_is_valid = False
                if number_is_valid == True:
                    data_list.append(int(number))
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None

        elif type == "tc" or type == "yes or no":
            for i in range(3):
                if type == "tc":
                    y_or_n = input(ui_element + "Do you agree to Terms and Conditions (y/n) : ")
                else:
                    y_or_n = input(ui_element + custom_message)
                if y_or_n not in ["y","n","Y","N"]:
                    box("The answer cannot be anything other than y,n,Y,N",escape_sequences = ui_element,warning_box = True)
                else:
                    data_list.append(y_or_n)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                return None

        elif type == "option":
            for i in range(3):
                option = input("\n" + ui_element + "Please enter an appropriate choice : ")
                if option.isdigit() == False:
                    box("Please enter an appropriate option",escape_sequences = ui_element,warning_box = True)
                    continue
                option = int(option)
                if option < option_range[0] or option > option_range[1]:
                    box("Please enter an appropriate option",escape_sequences = ui_element,warning_box = True)
                    continue
                else:
                    data_list.append(option)
                    all_tries_failed = False
                    break
            if all_tries_failed == True:
                box("You used all tries !\nPlease try again",escape_sequences = ui_element,error_box = True)
                return None
    if len(data_list) == 1:
        return data_list[0]
    return data_list

#block end 

#fucntion block for custom table
"""
This is indended as a custom function which can draw tables for this program and the tables drawn will change according to the arguments passed 

-- a input_list is passed first which can be nested list or not nested
-- passing a table name as argument will draw headers with the feilds of the table if its valid in database shipproject
-- passing valid escape_sequences will allow table to follow escape Sequences
-- passing a valid charecter to custom_corner will draw table with that corner
-- passing valid string into table_headers will draw table with it as a head while list_only is true
-- if list only is true it will draw single column table (nested list is not allowed here)
-- enabling full_lined will draw tables with lines in between after the headers
-- enabling numbered will draw numbered single column tables
-- enabling bulleted by giving it a valid charecter to use as bullets wull draw bulleted single column tables
-- enabling warning box draws a box with "!" containing the content passed into input_string indicating warning 
-- enabling error_box draws a box with "#" containing the content passed into input_string indicating a error
"""
def box(input_data,table_name = "NA",escape_sequences = "",custom_corner = "o",table_headers = "NA",list_only = False,full_lined = False,numbered = False,bulleted = "NA",warning_box = False, error_box = False,menu = False):
    
    escape_sequences = "\n" + escape_sequences #this is beacuse i want a newline before any table or box

    input_string = "NA"     #this is would mean you can pass data without worrying about list or strings 
    if type(input_data) is str:
        input_string = input_data
    elif type(input_data) is list:
        input_list = input_data

    #this will take advantage of single column table drawing part if the function and line2
    if input_string != "NA":
        list_only = True
        if menu == True:
            input_list = input_string.split("\n")
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "|"
            box_char2 = "-"
        elif warning_box == True: 
            input_list = input_string.split("\n")
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "+"
            box_char2 = "+"
            custom_corner = "+"
        elif error_box == True:
            input_list = input_string.split("\n")
            input_list.insert(0," ")
            input_list.append(" ")
            box_char = "#"
            box_char2 = "#"
            custom_corner = "#"
    else:
        box_char = "|"
        box_char2 = "-"


    #prints the table lines for [()]    (rows and columns)
    def line1():
        print(escape_sequences+custom_corner+"-",end="")
        for column in range(0,column_no):
            print("-"*lengthiest_data_list[column],end="")
            if column==column_no-1:
                print("-"+custom_corner)
                break
            print("-"+custom_corner+"-",end="")

    #prints the table lines for []  (single column)
    def line2():
        print(escape_sequences + custom_corner + box_char2,end="")
        print(box_char2 * lengthiest_data,end="")
        print(box_char2 + custom_corner)

    #calculates the padding and prints it along for [()] (rows and columns)
    def calc_padding1(row,column,content):
        padding_length=lengthiest_data_list[column]-len(str(input_list[row][column]))    
        content+=" "*padding_length
        return content

    #calculates the padding and prints it along for [] (single column)
    def calc_padding2(index,content):
        padding_length=lengthiest_data-len(str(input_list[index]))
        padding=" "*padding_length
        content+=padding
        return content

    #takes normal list for table conversation
    if list_only==True:
        
        #inserts table headers if present same like below but diffrent value which take input
        if table_headers!="NA":
            input_list.insert(0,table_headers)

        #for numbered single column tables
        if numbered == True:
            if table_headers == "NA":   #makes an exception for numbering if headers are given
                for index in range(0,len(input_list)):
                    number = str(index+1) + "."
                    input_list[index] = number + input_list[index]
            else:
                for index in range(1,len(input_list)):
                    number=str(index) + "."
                    input_list[index] = number + input_list[index]

        #for bulleted single column tables
        if bulleted != "NA":
            for index in range(1,len(input_list)):
                input_list[index] = bulleted + " " + input_list[index]

        #sets number of columns 
        index_count=len(input_list)

        #creates a variable named lengthiest_data containing the largest data length in the whole list
        lengthiest_data=0   #common for both variants of tables
        for index in range(0,index_count):
            if len(input_list[index]) > lengthiest_data:
                lengthiest_data=len(input_list[index])

        #prints the single columed table variant
        line2()
        escape_sequences=escape_sequences.replace("\n","")
        for index in range(0,index_count):
            if index==0 and table_headers!="NA":
                content=escape_sequences + box_char + " " + input_list[index]
                content=calc_padding2(index,content)
                content += " " + box_char
                print(content)
                line2()
            else:
                content = escape_sequences + box_char + " " + input_list[index]
                content = calc_padding2(index,content)
                content+=" " + box_char
                print(content)
                if full_lined==True:    #activates if full_lined is enabled
                    line2()
        if full_lined==False:
            line2()

    #prints the table variant with rows and columns
    if list_only==False:
        #sets number of rows and number of columns
        row_no=len(input_list) 
        column_no=len(input_list[0])

        #inserts table headers if table name given
        if table_name!="NA":
            table_headers=[]    
            cur1.execute("desc "+table_name)
            table_desc=cur1.fetchall()
            for desc_row in range(0,len(table_desc)):
                table_headers.append(table_desc[desc_row][0])
            input_list.insert(0,table_headers)
            row_no=len(input_list) 
            column_no=len(input_list[0])
            headers_flag=0
        else:
            headers_flag=1

        #creates a list named lengthiest_data_list containing the largest data lengths in each column 
        lengthiest_data_list=[]
        for column in range(0,column_no):
            lengthiest_data=0
            for row in range(0,row_no):
                if len(str(input_list[row][column]))>lengthiest_data:
                    lengthiest_data=len(str(input_list[row][column]))
            lengthiest_data_list.append(lengthiest_data)

        #actual part which converts to table
        line1()
        escape_sequences=escape_sequences.replace("\n","")
        for row in range(0,row_no):
            full_content=""     #this is done so that no error occurs in idle since all data is stored in ram before printing
            for column in range(0,column_no):
                if column==0:
                    content=escape_sequences+"| "
                    content+=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" | "
                    full_content+=content
                    continue
                if column==column_no-1 and headers_flag==0:
                    content=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" |"
                    full_content+=content
                    print(full_content)
                    line1()
                    headers_flag=1
                    continue
                if column==column_no-1:
                    content=str(input_list[row][column])
                    content=calc_padding1(row,column,content)
                    content+=" |"
                    full_content+=content
                    print(full_content)
                    if full_lined==True:
                        line1()
                    continue
                content=str(input_list[row][column])
                content=calc_padding1(row,column,content)
                content+=" | "
                full_content+=content
        if full_lined==False: #activates if full_lined is enabled
            line1()
#block end

# function block for loggging something
def log(log_input,escape_sequences="",error=False):
    timestamp=str(datetime.now())[:23:]     #sliced the string to avoid too much precision
    if error==True:
        l=open("error_log.txt","a") #if it was a error which was not intented for user will be logged in error_log.txt
    else:
        l=open("log.txt","a") #if it was a normal log it will be logged here but still wont be showed to user
    l.write(escape_sequences+"["+timestamp+"] "+log_input+"\n")
    l.close()
if module_error_flag==True: #logs import errors if any 
    log(module_error,error=True)
# block end 

# Function blocks end here 











# actual command line interface code

first_run() # Routes you back to the intialization run of the program in theroy this function runs first 

#main menu
print("\n")
print("               __-------___")
print("             _(            )__----- _")
print("            (  --Developed by        )")             # just an ASCII art for looks
print("             (___    foxpupfr         )_")
print("                 (___       on          )")
print("                     (__       github    ) ")
print("                         (__      _   _  ) \t\t#-----------------------------------------------#")
print("                            (    ) (  )(  )\t\t|                                               |")
print("                            (   )   ( ) ( )\t\t|      WELCOME TO SHIP MANANGEMENT SOFTWARE     |")
print("                             ( )  ()( ) ( )\t\t|                                               |")
print("                             __    __    __\t\t#-----------------------------------------------#")
print("                            |==|  |==|  |==|")
print("                          __|__|__|__|__|__|__")
print("                        __|___________________|___")     # I copied that table from my own box funtion
print("                     __|__[]__[]__[]__[]__[]__[]__|___")
print("                    |............................o.../")
print(r"""                    \.............................../""")     #this is a raw string if you are wondering
print("               hjw_,~')_,~')_,~')_,~')_,~')_,~')_,~')/,~')_")


#all of these are just menus made into functions
def login_menu():
    ui_element = "\t"
    log("user entred login menu")
    box("1.login\n2.staff login\n3.go back to main menu",escape_sequences = ui_element, menu = True)
    opt = input("\n" + ui_element + "Please enter an option (1-3) : ") 
    if opt == "1":
        log("user choosed normal login")
        login_status, user_id = login(ui_element) #redirects you to login and catches the value it returns 
        return login_status, user_id
    elif opt == "2":
        log("user choosed staff login")
        login_status, user_id = staff_login(ui_element)   #redirects you to login as above and does same but for staff
        return login_status, user_id
    elif opt == "3":
        log("user returned to main menu")
        return "exit", None #redirects you back to the main menu
    else:
        box("Please enter an appropriate option", escape_sequences = ui_element, warning_box = True)
        return "login_failed", None #also redirects you back to menu

def customer_menu(user_id):
    ui_element = "\t\t"
    log("customer with user ID " +str(user_id) + " entered customer menu")
    box("1.Book tickets\n2.See Tickets\n3.Prebooking\n4.Food Booking\n5.Go Back to main menu", escape_sequences = ui_element, menu = True)
    opt = data_catching(["option",], ui_element, option_range = (1,5))
    if opt == 1:
        log("user is trying to book ticekts feature")
        book_ticket(user_id, ui_element)
    elif opt == 2:
        log("user is using the see tickets feature")
        see_tickets_for_user(user_id, ui_element)
    elif opt == 3:
        log("user is using prebooking feature")
        book_ticket(user_id, ui_element, booking_type = "prebooking")
    elif opt == 4:
        log("user is using book food feature")
        book_food(user_id, ui_element)
    elif opt == 5:
        log("user exited customer menu")
        return "exit"

def staff_menu(login_status):
    ui_element = "\t\t"
    box("1.Deactivate Ticket\n2.Refund Ticket\n3.See Ship Info (Current)\n4.See Ship Info (Prebooking)\n5.See Ship History\n6.See Ticket History\n7.Adminstrative Menu\n8.Go Back",escape_sequences = ui_element, menu = True)
    opt = data_catching(["option",], ui_element, option_range = (1,8))
    if opt == 1:
        update_ticket(ui_element,user_type = "staff",update_type ="deactivate")
    if opt == 2:
        update_ticket(ui_element,user_type = "staff",update_type ="refund")   
    if opt == 3:
        see_info(ui_element,"ship info-currenta")
    if opt == 4:
        see_info(ui_element,"ship info-prebooking")
    if opt == 5:
        see_info(ui_element,"ship history")
    if opt == 6:
        see_info(ui_element,"ticket history")
    while login_status == "logged_in-admin" and opt == 7:
        box("--- Admin Menu ---\n \n1.Add Staff\n2.Remove Staff\n3.Use Databse Console With Admin Privilages\n4.Go Back",escape_sequences = ui_element, menu = True)
        sub_menu_opt = data_catching(["option",], ui_element, option_range = (1,4))
        if sub_menu_opt == 1:
            staff_registeration(ui_element,privilage_level = "admin",staff_type_to_add = "staff")
        if sub_menu_opt == 2:
            remove_staff(ui_element, privilage_level = "admin", staff_type_to_remove = "staff")
        if sub_menu_opt == 3:
            database_console(ui_element,"admin")
        if sub_menu_opt == 4:
            break
    while login_status == "logged_in-owner" and opt == 7:
        box("--- Owner Menu ---\n \n1.Add Staff\n2.Remove Staff\n3.Add Admin\n4.Remove Admin\n5.Use Databse Console With Admin Privilages\n6.Go Back",escape_sequences = ui_element, menu = True)
        sub_menu_opt = data_catching(["option",], ui_element, option_range = (1,6))
        if sub_menu_opt == 1:
            staff_registeration(ui_element,privilage_level = "owner",staff_type_to_add = "staff")
        if sub_menu_opt == 2:
            remove_staff(ui_element, privilage_level = "owner", staff_type_to_remove = "staff")
        if sub_menu_opt == 3:
            staff_registeration(ui_element,privilage_level = "owner",staff_type_to_add = "admin")
        if sub_menu_opt == 4:
            remove_staff(ui_element, privilage_level = "owner", staff_type_to_remove = "admin")
        if sub_menu_opt == 5:
            database_console(ui_element,"owner")
        if sub_menu_opt == 6:
            break
    if opt == 8:
        return "exit"
#all menu functions end here    

while con1.is_connected() == True:   # This puts program into loop untill user quits
    ui_element = " "
    log("user entered the main program")   
    print("\n\n" + ui_element  + "Please log in or register ( chose options 1, 2, 3 ) :")
    box("1.log in\n2.register ( If you don't have an account already )\n3.exit program",escape_sequences = ui_element,menu = True)
    
    opt=input("\n" + ui_element + "Please enter 1, 2, 3 : ") #opt will be used for main menu options
    if opt not in ["1","2","3"]:
        box("Please enter an appropriate option", escape_sequences = ui_element, warning_box = True)

        #login menu and sub menus
    while opt == "1":
        login_status, user_id = login_menu()
        if login_status == "exit":
            break
        while login_status == "logged_in-user":
            exit_status = customer_menu(user_id)
            if exit_status == "exit":
                break
        while login_status in ["logged_in-staff","logged_in-admin","logged_in-owner"]:
            exit_status = staff_menu(login_status)
            if exit_status == "exit":
                break
        #login menu and sub menus end    
        

        #registeration menu 
    while opt == "2":
        log("user choose registeration option")
        ui_element = "\t"
        box("1.Register\n2.Go Back To Main Menu",escape_sequences = ui_element, menu = True)
        opt_0 = data_catching(["option",], ui_element, option_range = (1,2))
        if opt_0 == 1:
            log("user entered registeration option further")
            user_reg_check = user_registeration(ui_element)
        if opt_0 == 2:
            log("user exited registeration menu")
            break
        if opt_0 == None: 
            log("user entered inappropriate option in register menu")
        #registeration menu end
        
        #program exit
    if opt =="3":
        log("user exited program")
        break




