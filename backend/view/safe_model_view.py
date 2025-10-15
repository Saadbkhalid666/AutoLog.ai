# safe_model_view.py
from flask_admin.contrib.sqla import ModelView #type:ignore
from flask_login import current_user #type:ignore
from wtforms.fields import SelectField #type:ignore

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        try:
            return current_user.is_authenticated and current_user.role == "admin"
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to admin login page
        from flask import redirect, url_for #type:ignore
        return redirect(url_for("admin_auth.login"))

class UserAdmin(BaseSecureModelView):

    form_excluded_columns = ('created_at', 'role',)
    can_create = False    
    can_delete = False

    def on_model_change(self, form, model, is_created):

        if is_created:
            model.role = "user"
        return super().on_model_change(form, model, is_created)
