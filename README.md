# Job Board

## Setup
- Enter your virtual environment: `source ~/virtualenv/bin/activate`
- Get the necessary libraries: `pip3 install -r requirements.txt`
- Run the script `python3 manage.py runserver`
- Check out Job Board at `http://127.0.0.1:8000/dashboard`

TODO:
- Technologies I used. 
Python3, Django framework.  
BCrypt - password hashing
Sqlite DB. Django's ORM for defining the classes / tables.

- What it does
Users can create an account to access a job board.  Users can post and accept jobs.
Owner of a job can edit or cancel the job.  Only the owner has the ability to cancel or log into a job thanks to authentication.

- Obstacles and learnings
Some of the more challenging and fun aspects of this projects were the validation and authentication layers.
I made sure that only valid users can update or delete the jobs they created.

- Screenshots of it working.
The dashboard when a user is logged in:
!["dashboard"](https://github.com/michelleshan/job_board/blob/master/assets/Screen%20Shot%202020-09-28%20at%203.01.22%20PM.png)

The edit job page:
!["edit job"](https://github.com/michelleshan/job_board/blob/master/assets/Screen%20Shot%202020-09-28%20at%203.01.51%20PM.png)

The log-in/registration page with a validation error message:
!["login"](https://github.com/michelleshan/job_board/blob/master/assets/Screen%20Shot%202020-09-28%20at%203.39.38%20PM.png)