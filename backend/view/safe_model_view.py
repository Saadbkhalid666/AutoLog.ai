# safe_model_view.py
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
import logging

logger = logging.getLogger(__name__)

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        # Check if user is authenticated and role is admin
        if current_user.is_authenticated and getattr(current_user, "role", None) == "admin":
            print("✅ Admin access granted")
            return True
        print(f"❌ Access denied | Authenticated: {current_user.is_authenticated}, Role: {getattr(current_user, 'role', None)}")
        return False

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to admin login if not accessible
        return redirect('/admin-login')
class UserAdmin(BaseSecureModelView):
    form_excluded_columns = ('created_at', 'role', 'password')
    can_create = False    
    can_delete = False
    column_exclude_list = ['password']
    column_list = ['id', 'username', 'email', 'role', 'created_at']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.role = "user"
        return super().on_model_change(form, model, is_created)