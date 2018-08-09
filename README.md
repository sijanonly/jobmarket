# Allwork



Allwork is a job marketplace. Job can be created by project owner and freelancers can apply to the project. Major components of the project

  - Users
  - Jobs
  - Inernal Direct message

# Users

  - User represent two types of user : (project owner and freelancer)
  - During signup, user need to select the user type (freelancer or project owner from the signup page)

# Jobs

  - Job owner can create jobs with different attributes(title, description, price, tags)
 

# Direct Message

  - Once project owner accept the proposal from a freelancer, a direct conversation will be started.

### Project Architecture

- While user is trying to register himself/herself to allwork, s/he needs to specifiy the user type (job owner, freelancer) and based on this selection two different identifier `is_owner` or `is_freelancer` will be set in user model.
- Once user is created, if the user is project owner, he can access `create job` page; he will need to put job title, job description, price, tags and even project document (optinal) to create project; which will put the job status to be `active`
- If the user is freelancer, he can see all jobs posted in the job list page.
- When a freelancer select a job, s/he will be directed to the job detail page and s/he can apply job by sending a proposal.
- The job owner can now see the number of job proposals on the Job detail page.
- Job owner will select / accept the proposal from the job detail page. When job owner click the proposal accept, the job status will be `running` and this acceptance will trigger the message to the freelancer and create a single chat room between freelancer and the job owner.
- In the same job detail page, project owner can close the project; which triggers the job status to be changed to `ended`
- For all `ended` project, the user will have `income` property, which will be calcuated as sum of price value of all the projects with `ended` status.
- Freelancer has their detail page, showing the `profile`, `skills ` and `total income`. S/he can also edit the details through `setting` dropdown menu.
- The system has `admin` section, which can be accessed through `/admin` path. The superuser/admin can easily create / change the user / job attributes from this section.


### Project setup


```sh
$ cd allwork
$ docker-compose up --build
$ docker-compose exec app python manage.py makemigrations
$ docker-compose exec app python manage.py migrate
```

