# # class Admin(models.Model):
# #     username = models.CharField(max_length=50)
# #     password = models.CharField(max_length=50)
# #
# #     def __str__(self):
# #         return f'{self.id}  {self.username}'
#
#
# class Employee(AbstractBaseUser):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # Add additional fields for the profile
#     time_card_nr = models.CharField(max_length=5, unique=True)
#     full_name = models.CharField(max_length=100)
#     mobile = models.CharField(max_length=10, blank=True)
#     dob = models.DateField(blank=True)
#     nationality = models.CharField(max_length=20, blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=20, null=False, unique=True)
#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['full_name', 'email', 'time_card_nr']
#     REQUIRED_FIELDS = ('user',)
#     USERNAME_FIELD = 'email'
#
#     def get_absolute_url(self):
#         """Returns the url to access a particular author instance."""
#         return reverse('user', args=[str(self.id)])
#
#     @property
#     def is_anonymous(self):
#         """
#         Always return False. This is a way of comparing User objects to
#         anonymous users.
#         """
#         return False
#
#     def __str__(self):
#         return f'{self.time_card_nr} {self.full_name} {self.user}'
#
#
# # class Employee(AbstractUser):
# #     time_card_nr = models.CharField(max_length=5, unique=True)
# #     full_name = models.CharField(max_length=100)
# #     mobile = models.CharField(max_length=10, blank=True)
# #     dob = models.DateField(blank=True)
# #     nationality = models.CharField(max_length=20, blank=True)
# #     address = models.CharField(max_length=100, blank=True)
# #     email = models.EmailField(max_length=20, null=False, unique=True)
# #     password = models.CharField(max_length=20)
# #     # USERNAME_FIELD = 'email'
# #
# #     def __str__(self):
# #         return f'{self.time_card_nr} {self.full_name}'
#
# # AUTH_USER_MODEL = 'office.Employee'