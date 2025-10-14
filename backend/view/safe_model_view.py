# safe_model_view.py
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms.fields import SelectField

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        try:
            return current_user.is_authenticated and current_user.role == "admin"
        except Exception:
            return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to admin login page
        from flask import redirect, url_for
        return redirect(url_for("admin_auth.login"))

class UserAdmin(BaseSecureModelView):
    # hide role from form so it can't be arbitrarily changed
    form_excluded_columns = ('created_at', 'role',)
    can_create = False    # optional - disable admin creation from admin panel
    can_delete = False

    def on_model_change(self, form, model, is_created):
        # Force non-admin users to 'user' role when created/edited via other flows (if any)
        if is_created:
            model.role = "user"
        return super().on_model_change(form, model, is_created)
