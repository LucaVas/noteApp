# NoteApp 
## Web note-taking application
### Built in HTML, CSS, JavaScript, Flask and SQL

#### Video Demo:  <https://youtu.be/3WK0WN4prdY>

#### Introduction:
NoteApp is a web application built in HTML, vanilla CSS and JavaScript for the front end, and Flask and SQL for the back end.

The idea was born by researching for inspirational project which would be not only challenging, but would result in practical and useful tools to use in my everyday life.

The application is structured with an initial registration and login method. Each user will be able to see only their own notes, and make any modifications on them.

Notes can be created, archived, and deleted. After a note is archived, it can be restored, but if it's deleted, it cannot be restored. Text editing features are added in through buttons, such as making text bold, italicized, striked-through and unerlined.

The application is responsive and can be used on any device.

#### Description:
The project is structured in several folders: main for application, 'static' for css files and js script, and 'templates' for the html pages.

I stuctured the style of the app into different CSS files, so that it would be easier to manipulate each part of the application separately. A main 'styles.css' allows to style overall unstyled elements.

I added media queries to make sure the application is responsive, and through styling choices such as 'display: none' I made sure some elements would appear and disappear depending on the device the app is displayed on.
If the application is run on a mobile or tablet display, the text secion is hidden and can be seen only by clicking on the proper button.

As the application runs with login mode, each user can see only their own notes, and any new user can register.

#### Structure:

Frontend
- Static folder containing CSS, images and JS files:
1. login.css : styles login and registration pages
2. navbar.css : styles the navigation bar (left or top section of page)
3. notes.css : style the central part of the page where notes are listed
4. text_section.css : styles the text editor part
5. script.js : contains JS script 

- templates folder containing HTML templates:
1. layout.html : main blueprint on which other pages are inserted
2. index.html : home page of applicaation
3. login.html : page for login
4. registration.html : page for registration

Backend:
1. app.py: main file where Flask application is contained
2. helpers.py : library file where login-required decorator is described
3. noteapp.db : Sqlite database containing all data of the application