from functools import wraps
from flask import session, redirect, url_for, flash
from models.seller import Seller


def seller_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        seller_id = session.get("seller_id")


        if not seller_id:
            flash(
                "Avval tizimga kiring",
                "warning"
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        seller = Seller.query.get(
            seller_id
        )


        if not seller:

            session.pop(
                "seller_id",
                None
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        if seller.status != "active":

            flash(
                "Hisobingiz hali tasdiqlanmagan",
                "danger"
            )

            return redirect(
                url_for(
                    "seller.login"
                )
            )


        return func(
            *args,
            **kwargs
        )


    return wrapper