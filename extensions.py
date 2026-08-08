from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# =====================================
# DATABASE
# =====================================

db = SQLAlchemy()



# =====================================
# LOGIN MANAGER
# =====================================

login_manager = LoginManager()


# Login kerak bo‘lsa qayerga yuboradi

login_manager.login_view = "auth.login"



# =====================================
# USER LOADER
# =====================================

@login_manager.user_loader
def load_user(user_id):

    try:

        user_id = int(user_id)


        # Avval oddiy user tekshiramiz

        from models.user import User

        user = User.query.get(
            user_id
        )


        if user:

            return user



        # Agar user bo‘lmasa admin tekshiramiz

        from models.admin import Admin

        admin = Admin.query.get(
            user_id
        )


        return admin



    except Exception as e:

        print(
            "LOGIN LOADER ERROR:",
            e
        )

        return None
