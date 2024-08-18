class Patient:
    """
    Days-Of-Week (DOW) enumerations:
    0 = Not Set
    1 = Everyday
    2 = Weekdays
    3 = Weekends

    Time-Of-Day (TOD) enumerations:
    0 = Not Set
    1 = Mornings (8am)
    2 = Noon (12pm)
    3 = Afternoon (4pm)
    4 = Evening (8pm)

    """

    patient_counter = 0  # class level variable

    def __init__(self, fname, lname, sms):
        self.first_name = fname
        self.last_name = lname
        self.sms_number = sms
        self.meds_list = []
        self.TOD_list = []
        self.DOW_list = []

        # counts the number of patients created
        Patient.patient_counter = Patient.patient_counter + 1

    def add_meds(self, med, tod, dow):
        global meds_list, TOD_list, DOW_list

        self.meds_list.append(med)
        self.TOD_list.append(tod)
        self.DOW_list.append(dow)
    def get_meds_list(self):
        return self.meds_list
    def get_TOD_list(self):
        return self.TOD_list
    def get_DOW_list(self):
        return self.DOW_list
    def get_SMS_number(self):
        return self.sms_number

    def get_patient_full_name(self):
        return self.first_name + ' ' + self.last_name
    def __str__(self):

        response = (f"\nPatient name: {self.first_name} {self.last_name} SMS Number: {self.sms_number}\n"
                    f"Meds list:\n")
        response3 = ''

        for index, med in enumerate(self.meds_list):
            TOD = ''

            times = self.TOD_list[index]
            if times == '1':
                TOD = '8am'
            elif times == '2':
                TOD = '12pm'
            elif times =='3':
                TOD = '4pm'
            elif times =='4':
                TOD = '8pm'
            else:
                TOD = 'not set'

            if self.DOW_list[index] == '1':
                DOW_tmp = 'everyday'
            elif self.DOW_list[index] == '2':
                DOW_tmp = 'weekdays'
            elif self.DOW_list[index] == '3':
                DOW_tmp = 'weekends'
            else:
                DOW_tmp = 'not set'

            response3 = response3 + (
                f"   {med} taken {len(self.TOD_list[index])} times per day at the following times: {TOD}"
                f"on the following days: "
                f"{DOW_tmp}.\n")

        return response + response3
