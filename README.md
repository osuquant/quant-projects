# quant-projects

Projects that I've worked on in my own-free time.

1.  TD Ameritrade API Project
- In this project I have created a class wrapper to retrieve and clean live option chain data efficiently.  I have also decided to use authenticated requests when I obtain data from the TD-Ameritrade API.  Although authenticated requests aren't currently required for the data I'm obtaining, it could be required in the future per their website. 

Class File:
- tdapi.py - contains the tdapi class object that I've created.  Each request for data requires use of the access token.  This class retrieves an initial authorization code which is used to obtain an access token and refresh token.  After you've used your access token you must obtain a new one via a post request with the refresh token.  
- Dependencies: splinter, requests, urllib, datetime, pandas, numpy


Functions:
- tdapi.tdapi(self, user, password, consumer_key, host, exec_path) - initializes a session with your TD Ameritrade username, password, consumer_key given from creating a developer app, host that you've chosen for your app, and exec_path of chromedriver so the splinter package can obtain the initial authentication code.  More details on these parameters shown under Other Files.  
- tdapi.option_chain(self, ticker, fromDate, toDate, cp) - function allows you to obtain live option chain information from any ticker from their database. 
- tdapi.option_unpack(self, data, cpflag) - option_chain data comes in a messy nested dictionary, this function unpacks the data into a more usable pandas dataframe.

Other Files:
- account.py - (NOT SHOWN), this file contains all the personal necessary information to start an api session.  Since it contains my username, password, and other pertinent info; I've decided to import these parameters from my local file.  Here is more info on these parameters:
- - user (str): TD Ameritrade username when you created an account
- - pass (str): TD Ameritrade password (could be different than your developer password)
- - consumer key (str, len = 32): consumer key given to you after you create an initial app
- - localhost (str): callback url that you specified, I used: http://localhost/test
- - exec_path (raw str): absolute path of where you installed chromedriver

- data_test.py - in this file I have shown a sample data retrieval, cleaning, and export to a dynamically named excel file.
- DIS_CALL_2019-07-23_2019-10-21.xlsx - result of the sample data retrieval in data_test.py, this is information of Disney Calls from 7/23/2019 to 10/21/2019.
