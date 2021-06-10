Travel Game

Travel Game Repository is a client-server application that provides a quiz based on the geolocation of a city. 
the application has system of login/register and a map that allows you to select a city .The application returns questions related to it
in this example the questions are inserted only about Naples, but user can create some questions about other cities

The application is developed using the following technologies:
SERVER-SIDE

    Python 3
    Flask framework
    SQLite 
    Mongodb

CLIENT-SIDE

    HTML, CSS ,JS



Software Requirements

    Python 3
    Flask
    SQLite
    Mongodb Compass Community 4.4.6

Configuration guide 

      to execute the app with pycharm, you need to install the following packages:
      
          1) Flask 
          2) FLask-Login
          3) Flask-emigrate
          4) Flask-pymongo
          5) Flask-WTF 
          6) Email-validator 
          7) Jwt 
      
      to install the packages in pycharm 
      open "FILE" - Setting-python-interpreter-click on 
      "+" and add packages
      
      Install Mongodb community 4.4.6 with the local service and 
      default ip 27017.

      After installation click on fill in connection fields 
     individually-create database with database name : "tecweb" 
     collection name : "tecweb". 
     Now add data and click insert document and in this document 
     past the content of file "domande.json" . 
     
     Launch the file run.py 
     with right mouse button and run the file 
     or, in terminal, using command:python run.py


     we suggest the use of pycharm educational edition to run 
     the application considering all dependeces.
     the application will be available on localhost:5000  
     To use service workers (that require a Secure Context)
     we choose localhost mode, instead of HTTPS

   
#Contributors
----------

- [Bernardo Iamicella] bernardo.iamicella001@studenti.unipartenope.it
- [Davide Carobene] davide.carobene001@studenti.unipartenope.it

If you have any issues, you can contact us.