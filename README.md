### Agenda

The goal of this test is to test Yahoo Mail Box.
More information is in `test_assignment` file.
Temporary account was created on Yahoo with credentials:  
user_login: asferrotest  
user_password: 9eqLiR8VgsR3t7Ta  
There is no intention to keep this account in the future, but
future test are required temporary account could be created 
again and credential should be changed in `locators` file

### Test environment: 

All required conf files are in root directory.
File named `locators` holds locators for By matcher, this
file also holds urls required to run the tests. Yahoo Account login and password

File named `settings` holds settings for tests and driver.  
It's possible to have comments in these files and empty strings. Comments must statr with `#`.

Test is using geckodriver and drivers binary shall be somewhere on testing machine.
`driver_exec_path` in settings file shall point to geckodriver.
`browser_profile` in settings file shall point to test profile for Mozilla Firefox.

### Test execution:

* Clone test to machine.
* Go to root directory.
* Run `python -m pip install -r requirements.txt`
* Run `pytest` in terminal. 