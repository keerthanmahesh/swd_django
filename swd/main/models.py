from django.db import models
from django.contrib.auth.models import User

MESS_CHOICES = (
    ('A','Dining Hall A'),
    ('C','Dining Hall C'))

CONSENT_CHOICES = (
    ('Letter', 'Letter'),
    ('Fax', 'Fax'),
    ('Email', 'Email')
    )

BONAFIDE_REASON_CHOICES = (
    ('Bank Loan', 'Bank Loan'),
    ('Passport', 'Passport'),
    ('Other', 'Other'))

BRANCH = {
    'A1': 'B.E.(Hons) Chemical Engineering',
    'A3': 'B.E.(Hons) Electrical and Electronics Engineering',
    'A4': 'B.E.(Hons) Mechanical Engineering',
    'A7': 'B.E.(Hons) Computer Science',
    'A8': 'B.E.(Hons) Electronics and Instrumentation Engineering',
    'B1': 'MSc. (Hons) Biology',
    'B2': 'MSc. (Hons) Chemistry',
    'B3': 'MSc. (Hons) Economics',
    'B4': 'MSc. (Hons) Mathematics',
    'B5': 'MSc. (Hons) Physics',
    'AA': 'B.E.(Hons) Electronics and Communication Engineering',
    'PH': 'PhD.',
    'H1': 'M.E. (Hons) Computer Science',

}

YEARNAMES = {
     0: 'First',
     1: 'Second',
     2: 'Third',
     3: 'Forth',
     4: 'Fifth',
}

STUDENT_STATUS = (
    ('Student', 'Student'),
    ('Thesis', 'Thesis'),
    ('PS2', 'PS2'),
    ('Graduate', 'Graduate'))

HOSTELS = (
    ('AH1', 'AH1'),
    ('AH2', 'AH2'),
    ('AH3', 'AH3'),
    ('AH4', 'AH4'),
    ('AH5', 'AH5'),
    ('AH6', 'AH6'),
    ('AH7', 'AH7'),
    ('AH8', 'AH8'),
    ('AH9', 'AH9'),
    ('CH1', 'CH1'),
    ('CH2', 'CH2'),
    ('CH3', 'CH3'),
    ('CH4', 'CH4'),
    ('CH5', 'CH5'),
    ('CH6', 'CH6'),
    ('CH7', 'CH7'),
)

class Warden(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    chamber = models.CharField(max_length=10, null=True, blank=True)
    residence = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hostel = models.CharField(max_length=5, choices=HOSTELS, null=True, blank=True)

    def __str__(self):
        return self.hostel + ' ' + self.name + ' ' + self.email + ' ' + self.chamber

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    staffType = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.staffType + ' ' + self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bitsId = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, blank=True)
    bDay = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bloodGroup = models.CharField(max_length=10, blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    admit = models.DateField(blank=True, null=True)
    parentName = models.CharField(max_length=50, blank=True, null=True)
    parentPhone = models.CharField(max_length=20, blank=True, null=True)
    parentEmail = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.bitsId + ' (' + self.name + ')'

class DayScholar(models.Model):
    student = models.OneToOneField('Student', on_delete = models.CASCADE)

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'

class HostelPS(models.Model):
    student = models.OneToOneField('Student', on_delete = models.CASCADE)
    acadstudent = models.BooleanField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS)
    psStation = models.CharField(max_length=20, null=True, blank=True)
    hostel = models.CharField(max_length=5, null=True, blank=True, choices=HOSTELS)
    room = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'

    def save(self, *args, **kwargs):
        if self.acadstudent == True:
            self.status = 'Student'
        super(HostelPS, self).save(*args, **kwargs)

class CSA(models.Model):
    student = models.OneToOneField('Student', on_delete = models.CASCADE)
    title = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.title + ' ' + self.student.name + self.email

class MessOption(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    monthYear = models.DateField()
    mess = models.CharField(max_length=1, choices=MESS_CHOICES)

    def __str__(self):
        return self.mess + ' ' + self.student.bitsId

class Bonafide(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    reason = models.CharField(max_length=20, choices=BONAFIDE_REASON_CHOICES)
    otherReason = models.CharField(max_length=20, null=True, blank=True)
    reqDate = models.DateField()
    printed = models.BooleanField(default=0, blank=True)
    text = models.TextField(default='', blank=True)

    def createText(self):
        gender = "Mr." if self.student.gender.lower() == 'm' else "Ms."
        pronoun = "He " if gender=="Mr." else "She "
        firstDeg=self.student.bitsId[4:6]
        secondDeg=self.student.bitsId[6:8]
        branch = BRANCH[firstDeg]
        if secondDeg != 'PS' and firstDeg != 'H1' and firstDeg != 'PH':
            branch = branch +' and '+ BRANCH[secondDeg]
        yearNum=self.reqDate.year-int(self.student.bitsId[0:4])
        if(self.reqDate.month <5):
            yearNum=yearNum-1
        yearName=YEARNAMES[yearNum]

        reason = self.otherReason if self.reason.lower()=='Other' else self.reason

        return '''This is to certify that ''' + gender +self.student.name.title() + ''', ID No.''' + self.student.bitsId + ''' is a bonafide student of '''+ yearName + ''' year at Birla Institute of Technology and Science (BITS) Pilani University, K.K Birla Goa campus, persuing ''' + branch + '''. This certificate is issued for the purpose of applying for ''' + reason + '''.'''

    def save(self, *args, **kwargs):
        if self.text == '':
            self.text = self.createText()
        super(Bonafide, self).save(*args, **kwargs)

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ') ' + self.reason

class Leave(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    dateTimeStart = models.DateTimeField()
    dateTimeEnd = models.DateTimeField()
    reason = models.TextField()
    consent = models.CharField(max_length=10, choices=CONSENT_CHOICES)
    corrAddress = models.TextField()
    corrPhone = models.CharField(max_length=15)
    approvedBy = models.ForeignKey('Warden', blank=True, null=True, on_delete="PROTECT")
    approved = models.BooleanField(default=0, blank=True)
    disapproved = models.BooleanField(default=0, blank=True)
    inprocess = models.BooleanField(default=1, blank=True)
    comment = models.TextField(default='', blank=True)

    def __str__(self):
        return self.student.bitsId + ' '+ self.student.name

class DayPass(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    dateTime = models.DateTimeField()
    reason = models.TextField()
    consent = models.CharField(max_length=10, choices=CONSENT_CHOICES)
    approvedBy = models.ForeignKey('Warden', blank=True, null=True, on_delete="PROTECT")
    approved = models.BooleanField(default=0, blank=True)
    disapproved = models.BooleanField(default=0, blank=True)
    inprocess = models.BooleanField(default=1, blank=True)
    comment = models.TextField()

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'

class LateComer(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    dateTime = models.DateTimeField()

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'

class InOut(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    place = models.CharField(max_length=20)
    outDateTime = models.DateTimeField()
    inDateTime = models.DateTimeField()
    onCampus = models.BooleanField()
    onLeave = models.BooleanField()

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'

class Disco(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    dateOfViolation = models.DateField()
    subject = models.TextField()
    action = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.student.bitsId + ' (' + self.student.name + ')'


class MessOptionOpen(models.Model):
    monthYear = models.DateField()
    dateOpen = models.DateField()
    dateClose = models.DateField()

    def __str__(self):
        return str(self.monthYear.month) + ' Open: ' + str(self.dateOpen) + ' Close: ' + str(self.dateClose)


class Transaction(models.Model):
    student = models.ForeignKey('Student', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.timestamp + ' ' + student.user

class MessBill(models.Model):
    month = models.DateField()
    amount = models.FloatField()
    rebate = models.FloatField()

    def __str__(self):
        return str(self.month) + ' ' + str(self.amount) + ' ' + str(self.rebate)
