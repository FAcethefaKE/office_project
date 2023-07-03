# # # class Admin(models.Model):
# # #     username = models.CharField(max_length=50)
# # #     password = models.CharField(max_length=50)
# # #
# # #     def __str__(self):
# # #         return f'{self.id}  {self.username}'
# #
# #
# # class Employee(AbstractBaseUser):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# #     # Add additional fields for the profile
# #     time_card_nr = models.CharField(max_length=5, unique=True)
# #     full_name = models.CharField(max_length=100)
# #     mobile = models.CharField(max_length=10, blank=True)
# #     dob = models.DateField(blank=True)
# #     nationality = models.CharField(max_length=20, blank=True)
# #     address = models.CharField(max_length=100, blank=True)
# #     email = models.EmailField(max_length=20, null=False, unique=True)
# #     # USERNAME_FIELD = 'email'
# #     # REQUIRED_FIELDS = ['full_name', 'email', 'time_card_nr']
# #     REQUIRED_FIELDS = ('user',)
# #     USERNAME_FIELD = 'email'
# #
# #     def get_absolute_url(self):
# #         """Returns the url to access a particular author instance."""
# #         return reverse('user', args=[str(self.id)])
# #
# #     @property
# #     def is_anonymous(self):
# #         """
# #         Always return False. This is a way of comparing User objects to
# #         anonymous users.
# #         """
# #         return False
# #
# #     def __str__(self):
# #         return f'{self.time_card_nr} {self.full_name} {self.user}'
# #
# #
# # # class Employee(AbstractUser):
# # #     time_card_nr = models.CharField(max_length=5, unique=True)
# # #     full_name = models.CharField(max_length=100)
# # #     mobile = models.CharField(max_length=10, blank=True)
# # #     dob = models.DateField(blank=True)
# # #     nationality = models.CharField(max_length=20, blank=True)
# # #     address = models.CharField(max_length=100, blank=True)
# # #     email = models.EmailField(max_length=20, null=False, unique=True)
# # #     password = models.CharField(max_length=20)
# # #     # USERNAME_FIELD = 'email'
# # #
# # #     def __str__(self):
# # #         return f'{self.time_card_nr} {self.full_name}'
# #
# # # AUTH_USER_MODEL = 'office.Employee'
#
# orm method="get" class="mb-3">
#     <div class="form-row">
#         <div class="col-md-4 mb-3">
#             <label for="order_by">Order By:</label>
#             <select name="order_by" id="order_by" class="form-control">
#                 <option value="id" {% if order_by == 'id' %}selected{% endif %}>ID</option>
#                 <option value="first_name" {% if order_by == 'first_name' %}selected{% endif %}>First Name</option>
#                 <option value="last_name" {% if order_by == 'last_name' %}selected{% endif %}>Last Name</option>
#                 <option value="time_card_nr" {% if order_by == 'time_card_nr' %}selected{% endif %}>Time Card Number</option>
#             </select>
#         </div>
#         <div class="col-md-4 mb-3">
#             <label for="order">Order:</label>
#             <select name="order" id="order" class="form-control">
#                 <option value="asc" {% if order == 'asc' %}selected{% endif %}>Ascending</option>
#                 <option value="desc" {% if order == 'desc' %}selected{% endif %}>Descending</option>
#             </select>
#         </div>
#         <div class="col-md-4 mb-3">
#             <button type="submit" class="btn btn-primary mt-4">Apply</button>
#         </div>
#     </div>
# </form>