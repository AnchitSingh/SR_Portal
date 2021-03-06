## SR Portal

SR Portal is an one stop platform for verifications of huge and large no. of csv files and pdf.

![Alt text](/screenshots/p8.png?raw=true "SR Portal")

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Documentation](#documentation)
- [Demo](#demo)
- [Screenshots](#screen)
- [License](#license)



## Installation

- This app requires python version>=3.8 .

### Clone

- Clone this repo to your local machine using `https://github.com/AnchitSingh/SR_Portal.git`

### Setup



> update and install these package first

```shell
$ pip3 install -r requirements.txt
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
- App can automatically detect corrupted csv. 
- Any no. of new courses can be added besides Phd and MTech.
- Feature to track how much time did Tutor spent on each document.
- Files are cross verified by two tutors before submission to manager.
- Only authorized person can have active account.
- Contains common platform for making annoucements.
- Cool and nice looking User Interface.
- 32 bit hashed passwords
## Usage 
- For first time use when no admin account exits go to <a href="http://127.0.0.1:5000/admin_register/1800" target="_blank">Admin Registration</a> page.
- Above link is accessible only if no admin account exists. 
- In the Upload section upload csv file with name as <course name>.csv (eg: phd.csv,mtech.csv ,btech.csv), then click on create database button and upload pdf files.


## Documentation
- You can view full documentation from  <a href="https://github.com/AnchitSingh/SR_Portal/blob/master/SRS%20SR_Portal.docx?raw=true" target="_blank">here</a>.

## Demo
- You can watch full demo video from  <a href="https://www.youtube.com/watch?v=yNZfGRWGFMQ" target="_blank">here</a>
---
## Screenshots
-Teaching Assistant verification window:
![Alt text](/screenshots/p61.png?raw=true "SR Portal")


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](https://raw.githubusercontent.com/AnchitSingh/SR_Portal/master/LICENSE)**
- Copyright 2020 © Anchit
