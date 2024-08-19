import sys
import datetime
import time
import requests

from patient import Patient

patients = []  # stores a list of patient objects

# uncomment for test stubs
'''P1 = Patient('rick', 'nelson', '3135551234')
P1.add_meds('asprin', '1', '1')
P1.add_meds('advil', '1', '2')
P1.add_meds('tylenol', '1', '3')
P1.add_meds('bayer2', '2', '1')
P1.add_meds('bayer2', '2', '2')
P1.add_meds('bayer2', '2', '3')
P1.add_meds('bayer3', '3', '1')
P1.add_meds('bayer3', '3', '2')
P1.add_meds('bayer3', '3', '3')
P1.add_meds('bayer4', '4', '1')
P1.add_meds('bayer4', '4', '2')
P1.add_meds('bayer4', '4', '3')

patients.append(P1)'''


def get_DOW_string(dow):
    if dow == '1':
        return 'Every Day'
    elif dow == '2':
        return 'Weekdays'
    elif dow == '3':
        return 'Weekends'
    else:
        return 'no DOW'


def get_TOD_string(tod):
    if tod == '1':
        return '8am'
    elif tod == '2':
        return '12pm'
    elif tod == '3':
        return '4pm'
    elif tod == '4':
        return '8pm'
    else:
        return 'no TOD'


def sendSMS(p, med, tod, dow):
    text_data = (
            'Hello ' + p.get_patient_full_name() + ' this is your medsSMS alert to remind you it is time for your ' +
            med + ' to be taken at ' + get_TOD_string(tod) + ' on this day ')
    headers = {
        'Authorization': 'Bearer ????', #requies authorization code
        'Content-Type': 'application/json',
    }

    json_data = {
        'from': '???', #provided by SMS provider
        'to': [
            '+1' + p.get_SMS_number(),
        ],
        'body': text_data,
    }

    # uncomment for test stub
    '''print(
        f'SMS Message sent to {p.get_patient_full_name()} @ {p.get_SMS_number()} for {med} to be taken at '
        f'{get_TOD_string(tod)} on this day {get_DOW_string(dow)}')'''

    # the following api has been provided as a trial service from www.sinch.com
    response = requests.post(
        'https://sms.api.sinch.com/xms/v1/5763b3fc8a8a413d907282a4574bdd0d/batches',
        headers=headers,
        json=json_data,
    )

    if response.status_code == '201':
        print(
            f'SMS Message sent to {p.get_patient_full_name()} @ {p.get_SMS_number()} for {med} to be taken at '
            f'{get_TOD_string(tod)} on this day {get_DOW_string(dow)}')
    else:
        print(f'Response status code ERROR: {response.status_code}')
        print(f'Response status code JSON: {response.json()}')


def checkDOW(dow, current):
    # current day of week is iso format
    # 1 = Monday
    # 2 = Tuesday
    # 3 = Wednesday
    # 4 = Thursday
    # 5 = Friday
    # 6 = Saturday
    # 7 = Sunday

    if dow == "2" and current <= 5:  # weekdays
        # send alert
        return True
    elif dow == "3" and current >= 6:  # weekdays
        # send alert
        return True
    elif dow == "1":  # everyday
        # send alert
        return True
    else:
        return False


def check_TOD(patients_list, current_tod, current_DOW):
    # check all patients for a valid TOD match; if valid then check for DOW match, if valid then send SMS
    for p in patients_list:
        tod_list = p.get_TOD_list()  # get list of times for this patient
        for index, tod in enumerate(tod_list):
            dow = p.get_DOW_list()[index]  # get the dow corresponding to the specific time index for this patient
            if str(current_tod) == tod:  # time match
                # check DOW
                if checkDOW(dow, current_DOW):
                    # send alert for this patient, med, and time.
                    sendSMS(p, p.get_meds_list()[index], tod, dow)


def scheduler(patients_list):
    flag_eight_am = False
    flag_twelve_pm = False
    flag_four_pm = False
    flag_eight_pm = False

    # this loop will execute every 55 seconds
    while True:
        print("\n*** Scheduler Active ***\n")
        # get time and day info
        current_time = datetime.datetime.now()
        current_DOW = current_time.isoweekday()
        current_minutes = current_time.minute
        current_hour = current_time.hour

        # test stub
        current_DOW = 1
        current_hour = 8
        current_minutes = 0

        # check current time against allowable time slots (8am, 12pm, 4pm, 8pm)
        if current_hour == 8 and current_minutes == 0 and not flag_eight_am:
            flag_eight_am = True  # this flag is used so that this time period is only checked once
            check_TOD(patients_list, 1, current_DOW)  # 1 = 8am
        elif current_hour == 12 and current_minutes == 0 and not flag_twelve_pm:
            flag_twelve_pm = True  # this flag is used so that this time period is only checked once
            check_TOD(patients_list, 2, current_DOW)  # 2 = 12pm
        elif current_hour == 16 and current_minutes == 0 and not flag_four_pm:
            flag_four_pm = True  # this flag is used so that this time period is only checked once
            check_TOD(patients_list, 3, current_DOW)  # 3 = 4pm
        elif current_hour == 20 and current_minutes == 0 and not flag_eight_pm:
            flag_eight_pm = True  # this flag is used so that this time period is only checked once
            check_TOD(patients_list, 4, current_DOW)  # 4 = 8pm
        else:
            # reset all flags
            flag_eight_am = False
            flag_twelve_pm = False
            flag_four_pm = False
            flag_eight_pm = False

        time.sleep(55)


def schedule_menu(patients_list):
    while True:
        print("\n==================================================\n")
        print("*** Scheduler Menu ***\n")
        print("1 = Run SMS scheduler")
        print("q = Return to main menu")
        menu_input = input('Enter Option==>')

        if menu_input == "1":
            if len(patients_list) == 0:
                print("\n*** No patients in list ***\n")
                return
            else:
                print("\n*** Scheduler Active ***\n")
                print("ctrl-c to stop application")
                scheduler(patients_list)


def add_patient():
    print("\n==================================================\n")
    print("*** Add Patient Menu ***\n")
    firstname = input("Enter First Name: ")
    lastname = input("Enter Last Name: ")
    smsinfo = input("Enter 10-digit phone number (include area code) that is able to receive text message alerts: ")

    print(f"\n --New patient added--\n")
    p = Patient(firstname, lastname, smsinfo)
    patients.append(p)
    return p


def add_meds(patient):
    while True:
        print("\n==================================================\n")
        print(f"Patient ID==> {patient.first_name} {patient.last_name}")
        print("*** Add Meds Menu ***\n")
        print("1 = Add medication to list")
        print("2 = Print current patients medication reminder list")
        print("q = Return to main menu")
        menu_input = input('Enter Option==>')

        if menu_input == "1":
            medname = input("Enter medication name: ")
            daysofweek = input("Enter Days of The Week: [1 = Everyday; 2 = Weekdays Only; 3 = Weekends Only] ==> ")
            timeofday = input(
                "Enter Time of Day for time to take medication: [1 = Mornings(8am); 2 = Noon(12pm); 3 = Afternoon("
                "4pm); 4 = Evening(8pm)] ==>")

            patient.add_meds(medname, timeofday, daysofweek)

        elif menu_input == "2":
            print(patient)
        elif menu_input == "q":
            return


def main():
    while True:
        print("\n==================================================\n")
        print("*** Main Menu ***\n")
        print("Select one of the following options: ")
        print("1 = Add Patient")
        print("2 = Run Schedule")
        print("3 = Print Patients List")
        print("q = Quit Program")
        main_input = input("Enter Option==> ")

        if main_input == "1":
            p = add_patient()
            add_meds(p)
        elif main_input == "2":
            schedule_menu(patients)
        elif main_input == "3":
            if len(patients) > 0:
                for e in patients:
                    print(f'\n{e}')
            else:
                print('\n==> No patients in system <==\n')
        elif main_input == "q":
            print(f'Patient Counter: {Patient.patient_counter}')
            sys.exit()


if __name__ == '__main__':
    main()
