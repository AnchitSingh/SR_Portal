from portal import app
from portal.extra_courses.BTECH.routes import BTECHs
app.register_blueprint(BTECHs)
from portal.extra_courses.gtech.routes import gtechs
app.register_blueprint(gtechs)
