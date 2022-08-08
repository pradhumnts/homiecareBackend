from django.db import models
from django.contrib.auth.models import AbstractUser
from statistics import mean
from .manager import CustomUserManager

class User(AbstractUser):
    username = None
    phoneNumber = models.CharField(max_length=25, unique=True)
    picture = models.ImageField(null=True, blank=True, default="media/5bb7fa59d4564e21a6f051b0578ff1b9.jpg")
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=155, blank=True, null=True)
    state = models.CharField(max_length=155, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    isNurse = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="secondary_address")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=155)
    state = models.CharField(max_length=155)
    country = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lat} - {self.long}"

class Review(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nurse")
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    review = models.TextField(max_length=2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_from} - {self.user_to}"

class Nurse(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    nurse_rating = models.FloatField(blank=True, null=True)
    convenience_fee = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1500, blank=True, null=True)
    alternate_phone = models.CharField(max_length=25, blank=True, null=True)
    working_distance_in_kms = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField(default=True, blank=True, null=True)
    verified = models.BooleanField(default=True, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

    @property
    def nurse_rating(self):
        if(len(Review.objects.filter(user_to=self.user))) > 0:
            return mean(Review.objects.filter(user_to=self.user).values_list("rating", flat=True))
        else: 
            return None

class Qualification(models.Model):

    MONTH_CHOICES = (
        ("JAN", "January"),
        ("FEB", "February"),
        ("MAR", "March"),
        ("APR", "April")
    )

    YEAR_CHOICES = (
        (2000, 2000),
        (2001, 2001),
        (2002, 2002),
        (2003, 2003)
    )

    DEGREE_CHOICES = ( 
    ("Bsc Nursing", "Bsc Nursing"),
    ("Bsc (Hons.) (Nursing)", "Bsc (Hons.) (Nursing)"),
    ("Post Basic Bsc Nursing", "Post Basic Bsc Nursing"),
    ("Bachelor of Science in Nursing(Post Certificate)", "Bachelor of Science in Nursing(Post Certificate)"),
    ("A.N.M.", "A.N.M."),
    ("G.N.M.", "G.N.M."),
    ("Advanced Diploma in Ophthalmic Care Management", "Advanced Diploma in Ophthalmic Care Management"),
    ("Diploma in Home Nursing", "Diploma in Home Nursing"),
    ("Diploma in Emergency and Trauma Care Technician", "Diploma in Emergency and Trauma Care Technician"),
    ("Diploma in Nursing Administraion", "Diploma in Nursing Administraion"),
    ("Diploma in Neuro Nursing", "Diploma in Neuro Nursing"),
    ("Diploma in Health Assistant(DHA)", "Diploma in Health Assistant(DHA)"),
    ("Certificate course in Ayurvedic Nursing", "Certificate course in Ayurvedic Nursing"),
    ("Certificate in Home Nursing", "Certificate in Home Nursing"),
    ("Certificate in Maternal and Child Health Care(CMCHC)", "Certificate in Maternal and Child Health Care(CMCHC)"),
    ("Certificate in Care Waste Management(CHCWM)", "Certificate in Care Waste Management(CHCWM)"),
    ("Certificate in Primary Nursing Management(CPNM)", "Certificate in Primary Nursing Management(CPNM)"),
    ("Msc Nursing", "Msc Nursing"),
    ("Msc in Child Health Nursing", "Msc in Child Health Nursing"),
    ("Msc in Community Health Nursing", "Msc in Community Health Nursing"),
    ("Msc in Medical-Surgical Nursing", "Msc in Medical-Surgical Nursing"),
    ("Msc in Maternity Nursing", "Msc in Maternity Nursing"),
    ("Msc in Paediatric Nursing", "Msc in Paediatric Nursing"),
    ("Msc in Obstetrics and Gyanecological Nursing", "Msc in Obstetrics and Gyanecological Nursing"),
    ("Msc in Psychiatric Nursing", "Msc in Psychiatric Nursing"),
    ("MD (Midwifery)", "MD (Midwifery)"),
    ("PhD (Nursing)", "PhD (Nursing)"),
    ("M Phil Nursing", "M Phil Nursing"),
    ("Post Basic Diploma in Critical Care Nursing", "Post Basic Diploma in Critical Care Nursing"),
    ("Post Basic Diploma in Orthopedic & Rehabilitation Nursing", "Post Basic Diploma in Orthopedic & Rehabilitation Nursing"),
    ("Post Basic Diploma in Operation Room Nursing", "Post Basic Diploma in Operation Room Nursing"),
    ("Post Graduate Diploma in paediatric Critical Care Nursing", "Post Graduate Diploma in paediatric Critical Care Nursing"),
    ("Post Basic Diploma in Ontological Nursing and Rehabilitation Nursing", "Post Basic Diploma in Ontological Nursing and Rehabilitation Nursing"),
    ("Post Gradute Diploma in Neo-Natal Nursing", "Post Gradute Diploma in Neo-Natal Nursing"),
    ("Post Graduate Diploma in Emergency Nursing","Post Graduate Diploma in Emergency Nursing")
    )

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    start_date_month = models.CharField(max_length=100, choices=MONTH_CHOICES, blank=True, null=True)
    start_date_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    end_date_month = models.CharField(max_length=100, choices=MONTH_CHOICES, blank=True, null=True)
    end_date_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nurse.user.phoneNumber

class Message(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=2000)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_from", blank=True, null=True)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_to", blank=True, null=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_from.first_name)

class PushNotificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name