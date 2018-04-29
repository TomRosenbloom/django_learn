# django_volcrm
This was my first attempt at learning Django.

The use-case is a volunteer matching and CRM system for voluntary sector organisations.

I made a fundamental error* in the way I structured my apps, so have put this aside now in favour of a new project in repository 'django_poets'.

Having said that, this project does have some interesting features:

- use of MPTT for categories of 'activity' and 'skill' which are used to match roles to volunteers
- calculation of 'roles within range' based on postcode and travel range of volunteer and postcode of role

Demo deployed here: http://tomrosenbloom.pythonanywhere.com/

\* The error was that I divided the project into apps based on some very broad areas of functionality in the system, so you see for e.g. apps called 'crm' and 'directory'. This is entirely the wrong way to do things and I've addressed that in the newer project.

