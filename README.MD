This project is a backend api project built with django and django rest framework(Python frameworks for backend web development).
It makes use of the JWT(Json Web Token) to authenticate users.
Its production and database are managed by render web hosting and database services.
The link to this project is https://edozie-drf-project-adqg.onrender.com

Currently, there are two main apps in this project.

One is the blogpost app, where a signed in user can create, read, update and delete posts.
Users who are not signed in can also read posts and post comments but are not permitted to create, update and delete posts.
The link to this app is https://edozie-drf-project-adqg.onrender.com/blogpost

The other app is a banking app that has the same features as a real life bank app.
When logged in, authenticated users can check their account balance, make transfer and view their statement of account.
The link to this app is https://edozie-drf-project-adqg.onrender.com/bankapp

Note: The blogpost app handles the user registration and login.

This is a backend project and you might not like how it displays on your screen(That's the job of a frontend developer).
To get the full workings of the project, i have added a python file(work.py) that helps you achieve that but you need to have a little knowledge of python to make it happen.
But if you have a good knowledge of postman, you can use postman to call the api endpoints.