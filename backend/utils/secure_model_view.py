from flask_admin.contrib.sqla import ModelView # type: ignore
from flask import session, redirect, url_for, request, jsonify # type: ignore

class SecureModelView(ModelView):
    def is_accessible(self):
        return "role" in session and session["role"] == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login", next=request.url)), jsonify({"message": "Access denied. Only Admins can Access this resource."}), 403
