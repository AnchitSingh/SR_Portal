## SR Portal

SR Portal is an one step platform for verifications of huge and large no. of csv files and pdf.

![Alt text](/screenshots/p9.png?raw=true "SR Portal")

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Screenshots](#screen)
- [License](#license)



## Installation

- This app requires python version>=3.8 .

### Clone

- Clone this repo to your local machine using `https://github.com/AnchitSingh/FlaskBeta.git`

### Setup



> update and install these package first

```shell
$ pip install -r requirements.txt
```

> 

```shell
$ python3 flask_app.py
```
- Click <a href="http://127.0.0.1:5000" target="_blank">here</a>
---

## Features

- Role Based Access Control.
- Option for automatic and manual allocation of files to Tutors.
- Any no. of new courses can be added besides Phd and MTech.
- Feature to track how much time did Tutor spent on each document.
- Files are cross verified by two tutors before submission to manager.
- Only authorized person can have active account.
- Contains common platform for making annoucements.
- Cool and nice looking User Interface.
- 32 bit hashed passwords
## Usage 
- For first time use when no admin account exits go to <a href="http://127.0.0.1:5000/admin_register/180085180200" target="_blank">Admin Registration</a> page.
- Above link is accessible only if no admin account exists. 
- In the Upload section upload csv file with name as <course name>.csv (eg: phd.csv,mtech.csv ,btech.csv), then click on create database button and upload pdf files.


## Documentation
- You can view full documentation from  <a href="https://github.com/AnchitSingh/FlaskBeta/blob/master/SR_Portal.docx?raw=true" target="_blank">here</a>.

---
## Screenshots
-Teaching Assistant verification window:
![Alt text](/screenshots/Screenshot from 2020-06-01 18-51-07.png?raw=true "SR Portal")


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © Anchit
