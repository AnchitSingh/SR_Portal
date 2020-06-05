import sqlite3
import os
import shutil
from flask import flash
def writedash_down(var):
    t='''
        <a href="{{url_for('phds.downloadphdCsv')}}">
            <button id="downbtn" class="btn btn-md btn-raised btn-round btn-rose">
                Phd csv
            </button>
        </a>
    '''
    f=open("portal/templates/dash_down.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/dash_down.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('downloadphdCsv', 'download'+var+'Csv')
    fin.close()
    fin = open("portal/templates/dash_down.html", "wt")
    fin.write(data)
    fin.close()


def writedash_sub(var):
    t='''
    {% for phd in phd%}
        {% if  current_user.is_admin==True or current_user.is_manager == True%}
        {% if phd[4] == 'Done' and phd[8] == 'Done' %}
        <tr>
           <td class="text-center">&bull;</td>
           <td>
              <h4>{{phd[0]}}</h4>
           </td>
           {% if phd[14] < 300 %}
           <td style="color:red;">
              <button type="button" style="background-color: transparent;border: none;" data-toggle="popover" title="Early Submission" data-content="{{phd[3]}} has submitted file within 5 minutes.Thus file might not been checked properly.">
              <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> {{phd[3]}}
              </button>
           </td>
           {% else %}
           <td>{{phd[3]}}</td>
           {% endif %}
           {% if phd[15] < 300%}
           <td style="color:red;">
              <button type="button" style="background-color: transparent;border: none;" data-toggle="popover" title="Early Submission" data-content="{{phd[2]}} has submitted file within 5 minutes.Thus file might not been checked properly.">
              <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> {{phd[2]}}
              </button>
           </td>
           {% else %}
           <td>{{phd[2]}}</td>
           {% endif %}
           <td class="text-center">PHD</td>
           <td class=" text-center">
              {% if phd[6] != 'Done' %}
              <a href="{{url_for('phds.lab_phd',application=phd[0])}}">
              <button class="btn btn-primary btn-sm">
              Verify
              </button>
              </a>
              {% else %}
              <a href="{{url_for('phds.lab_phd',application=phd[0])}}">
              <button style="background-image: linear-gradient(#ffa726, #fb8c00);" class="btn btn-sm">
              Verified
              </button>
              </a>
              {% endif %}
           </td>
        </tr>
        {% endif %}
        {% endif %}
        {% endfor %}
        '''
    f=open("portal/templates/dash_sub.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/dash_sub.html", "rt")
    data = fin.read()
    data = data.replace('{% endblock content %}', ' ')
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/templates/dash_sub.html", "wt")
    fin.write(data)
    fin.close()


def Data(var):
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute('''
        CREATE TABLE '''+var+''' (
            "Application Ref. No." INTEGER
        );''')
    c.execute('''ALTER TABLE '''+var+''' ADD Comment2 TEXT''')
    c.execute('''ALTER TABLE '''+var+''' ADD Submission2 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD Reject_Reason TEXT''')
    c.execute('''ALTER TABLE '''+var+''' ADD Validation TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD Comment1 TEXT''')
    c.execute('''ALTER TABLE '''+var+''' ADD Submission1 TEXT DEFAULT "Pending" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD Tutor1 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD Tutor2 TEXT DEFAULT "Not Assigned" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD alloc_status TEXT DEFAULT "0" ''')
    c.execute('''ALTER TABLE '''+var+''' ADD Application TEXT''')
    c.execute('''update '''+var+''' set Application = "Application Ref. No."; ''')
    conn.commit()
    conn.close()
    return


def writelab(var):
    fin = open("portal/extra_courses/"+var+"/templates/lab_"+var+".html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/extra_courses/"+var+"/templates/lab_"+var+".html", "wt")
    fin.write(data)
    fin.close()

def writeadmin(var):
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_admin.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_admin.html", "wt")
    fin.write(data)
    fin.close()


def writeta(var):
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_ta.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_ta.html", "wt")
    fin.write(data)
    fin.close()


def writedash(var):
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_submissions.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/extra_courses/"+var+"/templates/"+var+"_submissions.html", "wt")
    fin.write(data)
    fin.close()


def writetalab(var):
    fin = open("portal/extra_courses/"+var+"/templates/ta_lab_"+var+".html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('PHD', var.upper())
    fin.close()
    fin = open("portal/extra_courses/"+var+"/templates/ta_lab_"+var+".html", "wt")
    fin.write(data)
    fin.close()




def writeit(var):
    fin = open("portal/extra_courses/"+var+"/routes.py", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('phdcsv', ''+var+'csv')
    data = data.replace('phdData', ''+var+'Data')
    data = data.replace('PHD', var.upper())
    data = data.replace('downloadphdCsv', 'download'+var+'Csv')
    fin.close()
    fin = open("portal/extra_courses/"+var+"/routes.py", "wt")
    fin.write(data)
    fin.close()



def writeworkspace(var):
    t='''
        <div class="col-md-6">
            <div class="card">
                <div class="card-header" style="text-align: center;">
                    <h4 class="card-title">phd Section</h4>
                </div>
                <div class="card-content" >
                    <div class="table-responsive table-sales" style="display: flex;justify-content: center; align-items: center;">
                        <a href="{{ url_for('phds.phd')}}"><button class="btn btn-rose btn-lg" >phd Files</button></a>
                    </div>
                </div>
            </div>
        </div>
    '''
    f=open("portal/templates/workspaceadd.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/workspaceadd.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    fin.close()
    fin = open("portal/templates/workspaceadd.html", "wt")
    fin.write(data)
    fin.close()

def writeextra(var):
    t='''      
                    <div class="col-md-6" style="position: relative;">
                        <div class="card card-pricing card-raised" style="width: 50%;position: relative;left: 20%;">
                            <div class="content">
                                <h4 class="card-title">Phd Submissions</h4>
                                <a href="{{url_for('phds.phd_submission')}}" class="btn btn-rose btn-round">Enter</a>
                            </div>
                        </div>
                    </div>
    '''
    f=open("portal/templates/extra_add.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/extra_add.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    fin.close()
    fin = open("portal/templates/extra_add.html", "wt")
    fin.write(data)
    fin.close()



def writereset(var):
    t='''
        <div class="col-lg-6">
            <div class="card card-pricing card-raised">
                <div class="content">
                    <h4 class="card-title">phd Database</h4>
                    <div class="icon icon-rose">
                        <span class="material-icons">
                            delete_sweep
                        </span>
                    </div>
                    <h3 class="card-title">DANGER</h3>
                    <p class="card-description">
                        Once deleted it can't be reverted back
                    </p>
                    <a href="{{url_for('phds.reset_phd')}}" class="btn btn-rose btn-round">Reset Phd</a>
                </div>
            </div>
        </div>
    '''
    f=open("portal/templates/resetadd.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/resetadd.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('phd', str(var))
    fin.close()
    fin = open("portal/templates/resetadd.html", "wt")
    fin.write(data)
    fin.close()


def writeupload_top(var):
    t='''
            <div class="modal fade" id="smallAlertModalphd" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-small ">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="material-icons">clear</i></button>
                        </div>
                        <div class="modal-body text-center">
                            <h5>Are you sure you want to submit? </h5>
                        </div>
                        <div class="modal-footer text-center">
                            <button type="button" class="btn btn-simple" data-dismiss="modal">Never mind</button>
                            <a href="{{url_for('phds.allocate_phd')}}"><button type="submit" class="btn btn-success btn-simple">Yes</button></a>
                        </div>
                    </div>
                </div>
                </div>
            <button class="btn btn-raised btn-round btn-rose" data-toggle="modal" data-target="#smallAlertModalphd">
                Allocate Phd
            </button>
    '''
    f=open("portal/templates/uploadadd_top.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/uploadadd_top.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    fin.close()
    fin = open("portal/templates/uploadadd_top.html", "wt")
    fin.write(data)
    fin.close()


def writeupload_bottom(var):
    t='''
    <a href="{{url_for('phds.phdcsv')}}">
        <button class="btn btn-raised btn-round btn-rose" >
            Create phd database
        </button>
    </a>
    '''
    f=open("portal/templates/uploadadd_bottom.html", "a+")
    f.write(t)
    f.close()
    fin = open("portal/templates/uploadadd_bottom.html", "rt")
    data = fin.read()
    data = data.replace('phd', str(var))
    data = data.replace('Phd', str(var))
    data = data.replace('phdcsv', ''+var+'csv')
    fin.close()
    fin = open("portal/templates/uploadadd_bottom.html", "wt")
    fin.write(data)
    fin.close()



def delete_courses():
    t=""
    shutil.rmtree('portal/extra_courses/')
    os.mkdir("portal/extra_courses/")
    f=open("portal/templates/uploadadd_bottom.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/uploadadd_top.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/workspaceadd.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/dash_down.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/dash_sub.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/resetadd.html", "w")
    f.write(t)
    f.close()
    f=open("portal/templates/extra_add.html", "w")
    f.write(t)
    f.close()
    f=open("portal/blueprints.py", "w")
    k="from portal import app\n"
    f.write(k)
    f.close()
    conn = sqlite3.connect('portal/site.db') 
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    courses=open("portal/records.txt","rt")
    for line in courses:
        c.execute('''drop table '''+line+''';''')
    conn.commit()
    conn.close()
    f=open("portal/records.txt", "w")
    f.write(t)
    f.close()
    return



def addRecord(var):
    f=open("portal/records.txt","a+")
    f.write(var+"\n")
    f.close()
    return