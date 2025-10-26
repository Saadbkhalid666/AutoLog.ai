# safe_model_view.py
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
import logging

logger = logging.getLogger(__name__)

class BaseSecureModelView(ModelView):
    form_excluded_columns = ('created_at',)

    def is_accessible(self):
        """Check if current user is authenticated and is admin"""
        try:
            is_auth = current_user.is_authenticated
            role = getattr(current_user, 'role', None)
            user_id = getattr(current_user, 'id', None)
            
            print(f"🔐 AUTH DEBUG - User ID: {user_id}, Authenticated: {is_auth}, Role: {role}")
            
            if is_auth and role == 'admin':
                print("✅ Access GRANTED to admin view")
                return True
            else:
                print("❌ Access DENIED to admin view")
                return False
                
        except Exception as e:
            print(f"🚨 Error in is_accessible: {e}")
            return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to frontend admin login page"""
        print("🔒 Redirecting to login page")
        return redirect('http://localhost:4200/admin-login')  # Your Angular login page

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