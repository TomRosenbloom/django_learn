# django_learn
This is me learning Django.

The use-case is a volunteer matching and CRM system for voluntary sector organisations.

There are five classes of user:

  - Admin (Django superuser login)

  - Public (no login) – can browse [and search] directory of organisations [and volunteer roles]

  - Volunteer (signup/login as volunteer) – create/edit profile and find matching roles

  - Organisation member (signup/login as organisation) – create/edit organisation profile and create roles

A user can be both a volunteer and an organisation member.


- Public – can browse and search directory of organisations [and volunteer roles]
-	Volunteer – sign up as volunteer then create/edit profile and find matching roles
-	Organisation member  – sign up as organisational user  to create/edit organisation profile and create roles
-	Volunteer Service officer – CRM system and administration of volunteer matching system
-	Django Admin – Django superuser login, for developers only

Features:

- Different varieties of CRUD functionality, depending on context
  - Generic CBVs
  - ‘pretty’ list/detail views in public directory, tabular listings with edit/deletelinks in CRM
  - Filter-search of list views and list tables
  - Enhanced pagination
  - Export results as CSV
- Separate sign up and login for different user types, with custom access
- Volunteer opportunities found for volunteers, based on their profile: skills and activities, [location and travel range]
- [Volunteers found for organisations]

Packages:

- Django-address
- Django-bootstrap
- Django-ckeditor
- Django-csvimport
- Django-filter
- Django-localflavor
- Django-MPTT – for managing models representing hierarchical categories e.g. the skills offered by prospective volunteers
- Django-pagination
- Django-select2-forms
- Django-tables2
- Django-widget-tweaks
