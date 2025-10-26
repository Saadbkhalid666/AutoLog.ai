from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        """Check if current user is authenticated and is admin"""
        try:
            is_authenticated = current_user.is_authenticated
            user_role = getattr(current_user, 'role', None)
            print(f"Auth Check - Authenticated: {is_authenticated}, Role: {user_role}")
            return is_authenticated and user_role == 'admin'
        except Exception as e:
            print(f"Auth check error: {e}")
            return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to frontend admin login page"""
        print("Access denied - redirecting to login")
        return redirect('/admin-login')  # Your Angular admin login page

class UserAdmin(BaseSecureModelView):
    form_excluded_columns = ('created_at', 'role', 'password')
    can_create = False    
    can_delete = False
    column_exclude_list = ['password']
    column_list = ['id', 'username', 'email', 'role', 'created_at']

    def on_model_change(self, form, model, is_created):
        try:
            if is_created:
                model.role = "user"
            return super().on_model_change(form, model, is_created)
        except Exception as e:
            print(f"Model change error: {e}")
            raise