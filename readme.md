Heart Care 
Heartcare is a diagonos c management project developed in django. Admin can add doctor, add 
services, add gallery pictures . User can see doctors profile and also they can make appointment. 
They can also contact to the heartcare through email. 
Admin Features: 
 Doctor Management: Add, edit, and manage doctor profiles 
 Service Management: Create and update diagnos c services offered 
 Gallery Management: Upload and manage gallery pictures 
 Appointment Oversight: View and manage pa ent appointments 
 User Management: Administer user accounts and permissions 
User Features: 
 Doctor Profiles: View detailed informa on about healthcare providers 
 Appointment Scheduling: Book appointments with doctors 
 Service Informa on: Browse available diagnos c services 
 Gallery Viewing: See facility images 
 Contact Func onality: Send emails to the Heartcare team 
Technical Implementa on 
This system would typically include: 
1. Models: 
o Doctor (name, specialty, bio, photo, etc.) 
o Service (name, descrip on, price) 
o Gallery (image, cap on) 
o Appointment (pa ent, doctor, date, me, status) 
o ContactMessage (name, email, subject, message) 
2. Views: 
o CRUD opera ons for admin management 
o Public views for users to browse content 
o Appointment booking system 
o Contact form handler 
3. Templates: 
o Admin dashboard 
o Public-facing pages (doctors, services, gallery) 
o Appointment booking form 
o Contact page 
4. Email Integra on: 
o Configura on for sending/receiving emails 
o Appointment confirma on emails 
o Contact form email no fica ons 
Summary of Skills Required 
Category 
Backend 
Frontend 
Database 
Technologies Used 
Python, Django, ORM 
HTML5, CSS3, Bootstrap, JavaScript, jQuery 
SQLite (Dev), PostgreSQL  
1. Backend (Django/Python) 
Core Technologies 
 Python: Primary programming language for Django development. 
 Django (v3.x/4.x): High-level Python web framework for rapid development. 
o Django ORM: For database interac ons (SQL queries abstracted into Python classes). 
o Django Admin: Built-in admin panel for managing doctors, services, and 
appointments. 
o Django Authen ca on: User registra on, login, and role-based permissions 
(admin/pa ent). 
Key Django Features Used 
 Models (models.py): 
o Doctor, Service, Appointment, Gallery, ContactMessage. 
 Views (views.py): 
o Class-based views (CBV) for CRUD opera ons. 
o Func on-based views for contact forms and appointments. 
 URL Rou ng (urls.py): 
o Path rou ng for different pages (doctors, services, etc.). 
 Forms (forms.py): 
o AppointmentForm, ContactForm with valida on. 
 Email Integra on (se ngs.py): 
o SMTP (Gmail/Outlook) for appointment confirma ons and contact form 
submissions. 
Database 
 SQLite (Development) / PostgreSQL (Produc on): 
o Stores doctor profiles, appointments, and user data. 
APIs (Op onal) 
 Django REST Framework (DRF): 
o If a mobile app or external integra ons are needed. 
2. Frontend (HTML/CSS/JavaScript) 
Core Technologies 
 HTML5: Structure of web pages (templates in hospital/, appointment/). 
 CSS3 & Bootstrap 5: 
o Responsive design (works on mobile, tablet, desktop). 
o Pre-styled components (bu ons, forms, cards). 
 JavaScript (Vanilla JS/jQuery): 
o Form valida on. 
o Dynamic content loading (AJAX for appointments). 
o Interac ve elements (sliders, galleries). 
Key Frontend Libraries 
 jQuery: Simplifies DOM manipula on and AJAX calls. 
 Lightbox2 (for gallery image popups). 
 Font Awesome: Icons for bu ons, social media, etc. 
 Google Fonts (Poppins/Roboto): Modern typography. 
Template Engine 
 Django Template Language (DTL): 
o {% extends 'base.html' %} for template inheritance. 
o {% for doctor in doctors %} loops to display dynamic data. 
o {% if user.is_authen cated %} for condi onal rendering. 
 
 
Project Structure Overview 
text 
templates/ 
├── admin/                     # Admin-specific templates 
│   └── base_site.html         # Customizes the admin site appearance 
├── appointment/ 
│   └── index.html             # Main appointment booking page 
├── hospital/                  # Core applica on templates 
│   ├── contact.html           # Contact form page 
│   ├── faq.html               # FAQ page 
│   ├── gallery.html           # Displays gallery images 
│   ├── index.html             # Homepage 
│   ├── service_details.html   # Detailed view of a single service 
│   ├── services.html          # List of all services 
│   ├── team_detail.html       # Detailed doctor profile 
│   └── team.html              # List of all doctors 
└── par als/                  # Reusable components 
    ├── _css.html               
    ├── _footer.html 
    ├── _header.html 
    ├── _js.html 
    ├── _pagina on.html 
    ├── _sidebar.html 
    ├── _slider.html 
    └── base.html              # Base template all others inherit from 
 
Detailed File Breakdown 
1. Admin Templates 
 admin/base_site.html 
o Customizes the Django admin interface (branding, tles) 
o Overrides the default admin base template 
2. Appointment Templates 
 appointment/index.html 
o Contains the appointment booking form 
o Shows available me slots, doctor selec on, and pa ent details 
3. Hospital (Main App) Templates 
 contact.html 
o Contact form with fields (name, email, message) 
o May include Google Maps integra on 
 faq.html 
o Displays frequently asked ques ons in an accordion/collapsible format 
 gallery.html 
o Grid layout of medical facility/team photos 
o Lightbox integra on for image previews 
 index.html (Homepage) 
o Hero sec on with slider (_slider.html) 
o Highlights key services, doctors, tesmonials 
o Calls-to-ac on for booking/appointments 
 service_details.html 
o Detailed view of a diagnos c service (descrip on, pricing, dura on) 
o Related services sec on 
 services.html 
o Grid/list of all healthcare services with brief info 
o Filtering/sor ng op ons if implemented 
 team.html 
o Displays all doctors with photos, special es, and brief bios 
o Links to individual doctor pages 
 team_detail.html 
o Full doctor profile (qualifica ons, experience, schedule) 
o "Book Appointment" bu on linking to appointment/index.html 
4. Par als (Reusable Components) 
 base.html 
o Master template containing <html>, <head>, <body> 
o Blocks: {% block content %}, {% block css %}, {% block js %} 
o Includes all par als (_header.html, _footer.html, etc.) 
 _css.html 
o All CSS imports (Bootstrap, custom styles, fonts) 
 _js.html 
o JavaScript files (jQuery, Bootstrap, custom scripts) 
 _header.html 
o Naviga on bar with logo, menu items (Home, Services, Doctors) 
o Login/Register bu ons or user dropdown 
 _footer.html 
o Copyright info, quick links, contact details 
o Social media icons 
 _sidebar.html 
o Op onal sidebar (may show in admin or user dashboard) 
o Filters for services/doctors if used 
 _slider.html 
o Homepage carousel with promo onal banners 
o Autoplay controls, indicators 
 _pagina on.html 
o Reusable pagina on controls for lists (doctors, services, gallery) 
Here's a step-by-step guide to run the Heartcare Django project 
1. venv\Scripts\ac vate                                           
2. python manage.py runserver                             
# Ac vate (Windows) 
#  Run the Development Server 
 Open your browser and go to: 
o Homepage: h p://127.0.0.1:8000/ 
o Admin Panel: h p://127.0.0.1:8000/admin (Login with superuser creden als.) 
 