# api/__init__.py


from flask import Blueprint


# API BLUEPRINT

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)



# ROUTES

from . import products
from . import auth
from . import categories
from . import cart

# =====================================
# VENDORA API PACKAGE
# =====================================







# =========================
# MODELS IMPORT
# =========================





# Keyingi API lar uchun:

# from . import cart
# from . import favorite
# from . import profile
# from . import seller