# safe_model_view.py
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        """Check if current user is authenticated and is admin"""
        return current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to your frontend admin login page"""
        return redirect('/admin-login')  # Your frontend admin login route

class UserAdmin(BaseSecureModelView):
    form_excluded_columns = ('created_at', 'role',)
    can_create = False    
    can_delete = False
    column_exclude_list = ['password']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.role = "user"
        return super().on_model_change(form, model, is_created)