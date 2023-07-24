Office Project

This application is designed to streamline task assignment and tracking within an office environment. This application empowers the office administrator with the ability to assign tasks to employees and keep track of their task status. One of the key features of this system is the real-time notification system that enables the office admin to know whether the assigned tasks have been read by the employees. 
The "Office Project" aims to improve office productivity and communication by providing a centralized platform for task management. 

Office Page
1. Employee Registration and Management
    • The admin can register new employees with their details, such as time card number, mobile, date of birth, nationality, and address.
    • The admin can view and manage all registered employees, including updating their information and deleting profiles.
2. Task Assignment
    • The admin can create tasks with titles, descriptions, and assign dates.
    • Tasks can be assigned to one or multiple employees at a time.
3. Real-time Task Assignment Confirmation
    • The system automatically generates task assignment confirmation field for each assigned task and employee.
    • The admin receives notifications when employees read their assigned tasks.
Employee Page
1. Employee Login
    • Employees can log in with their registered email and password to access their personalized dashboard.
2. Employee Task Dashboard
    • Employees have access to a task dashboard displaying their assigned tasks.
    • Tasks are organized by assign date and can be filtered to show only current or all tasks.
3. Task Status and Mark as Read
    • Employees can view the status of their assigned tasks, including whether they have read the task or not.
    • Employees can mark tasks as "Read" to confirm acknowledgment of the assignment.
4. Personal Information
    • Employees can view their personal information provided during registration.
    • The information is read-only and can only be updated by the admin.
5. Change Password
    • Employees can change their account password securely.
Installation and Setup
To run the "Office Project" application locally, follow these steps:
    1. Clone the repository from GitHub.
    2. Set up a virtual environment and activate it.
    3. Install the required dependencies using pip install -r requirements.txt.
    4. Set up the database and run migrations using 
       python manage.py makemigrations
       python manage.py migrate.
    5. Create a superuser for admin access using python manage.py createsuperuser.
    6. Start the development server with python manage.py runserver.
    7. Access the admin page at http://127.0.0.1:8000/admin/ to log in as the admin and manage employees and tasks.
    8. Employees can access their dashboard at http://127.0.0.1:8000/employee_login/ and log in with their registered email and password.
Technologies Used
Application is built using Django, a Python web framework. The application utilizes Django's authentication system, models, forms, and views to manage user registration, task assignment, and task tracking.
Author
    • Agne Grinceviciute
      
For any inquiries or issues, please contact agne.grin@gmail.com
