from flask_admin.contrib.sqla import ModelView

class SafeModelView(ModelView):
    form_excluded_columns = []   