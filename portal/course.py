import os 
import sqlite3
from portal.helper_code.helper import writedash_down,writedash_sub,writeworkspace,writeta,writeupload_top,Data,addRecord
from portal.helper_code.helper import writeadmin,writeit,writelab,writereset,writetalab,writeupload_bottom,writedash,writeextra
from flask import flash

def cdir(var):
    directory = "portal/extra_courses/"+str(var)
    directory2 = "portal/"+str(var)
    directory3 = "portal/extra_courses"
    if os.path.exists(directory3):
        pass
    else:
        os.mkdir(directory3)
    if os.path.exists(directory):
        flash('Course already exists','danger')
    elif os.path.exists(directory2):
        flash('Course already exists','danger')
    else:
        os.mkdir(directory)
        addRecord(var)
        p = directory+"/templates"
        os.mkdir(p)
        with open("portal/base/routes.py") as f:
            with open("portal/extra_courses/"+var+"/routes.py","w+") as f1:
                for line in f:
                    f1.write(line)
        writeit(var)
        with open("portal/phd/templates/lab_phd.html") as f:
            with open("portal/extra_courses/"+var+"/templates/lab_"+var+".html","w+") as f1:
                for line in f:
                    f1.write(line)
        writelab(var)
        with open("portal/phd/templates/phd_admin.html") as f:
            with open("portal/extra_courses/"+var+"/templates/"+var+"_admin.html","w+") as f1:
                for line in f:
                    f1.write(line)
        writeadmin(var)
        with open("portal/phd/templates/phd_ta.html") as f:
            with open("portal/extra_courses/"+var+"/templates/"+var+"_ta.html","w+") as f1:
                for line in f:
                    f1.write(line)
        writeta(var)
        with open("portal/base/templates/submissions.html") as f:
            with open("portal/extra_courses/"+var+"/templates/"+var+"_submissions.html","w+") as f1:
                for line in f:
                    f1.write(line)
        writedash(var)
        with open("portal/phd/templates/ta_lab_phd.html") as f:
            with open("portal/extra_courses/"+var+"/templates/ta_lab_"+var+".html","w+") as f1:
                for line in f:
                    f1.write(line)
        writetalab(var)
        writeextra(var)
        writeworkspace(var)
        writereset(var)
        writeupload_top(var)
        writeupload_bottom(var)
        writedash_down(var)
        writedash_sub(var)
        f=open("portal/blueprints.py", "a+")
        f.write("from portal.extra_courses."+var+".routes import "+var+"s\napp.register_blueprint("+var+"s)\n")
        Data(var)
        flash('New Course added','success')

