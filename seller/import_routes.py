import os
import json

from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    render_template,
    session,
    send_file
)

from werkzeug.utils import secure_filename

from models.seller import Seller

from utils.excel_import import import_products
from utils.excel_template import create_product_template
from utils.excel_error import create_error_excel


seller_import = Blueprint(
    "seller_import",
    __name__,
    url_prefix="/seller/products"
)


UPLOAD_FOLDER = "uploads/excel"

ALLOWED_EXTENSIONS = {
    "xlsx"
}


# ==================================
# CHECK FILE
# ==================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )



# ==================================
# EXCEL IMPORT
# ==================================

@seller_import.route(
    "/excel",
    methods=[
        "GET",
        "POST"
    ]
)
def excel_import():


    if request.method == "POST":


        file = request.files.get(
            "file"
        )


        if not file:

            flash(
                "Excel fayl tanlanmagan",
                "danger"
            )

            return redirect(
                url_for(
                    "seller_import.excel_import"
                )
            )



        if not allowed_file(
            file.filename
        ):

            flash(
                "Faqat .xlsx fayl yuklash mumkin",
                "danger"
            )

            return redirect(
                url_for(
                    "seller_import.excel_import"
                )
            )



        # =========================
        # SELLER CHECK
        # =========================


        seller_id = session.get(
            "seller_id"
        )


        if not seller_id:

            flash(
                "Avval seller hisobiga kiring",
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

            flash(
                "Seller topilmadi",
                "danger"
            )

            return redirect(
                url_for(
                    "seller.dashboard"
                )
            )



        # =========================
        # SAVE FILE
        # =========================


        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )


        filename = secure_filename(
            file.filename
        )


        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        file.save(
            file_path
        )



        # =========================
        # IMPORT
        # =========================


        result = import_products(
            file_path,
            seller.id
        )



        success = result.get(
            "success",
            0
        )


        errors = result.get(
            "errors",
            []
        )



        if success:

            flash(
                f"{success} ta mahsulot qo'shildi",
                "success"
            )



        if errors:

            flash(
                f"{len(errors)} ta qatorda xato topildi",
                "warning"
            )


            session["excel_errors"] = errors



        return redirect(
            url_for(
                "seller.products"
            )
        )



    return render_template(
        "seller/product_excel.html"
    )





# ==================================
# DOWNLOAD TEMPLATE
# ==================================


@seller_import.route(
    "/excel/template"
)
def excel_template():


    file = create_product_template(
        session.get(
            "seller_id"
        )
    )


    return send_file(
        file,
        as_attachment=True,
        download_name=
        "Sotuv_Biznes_Product_Template.xlsx",

        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )





# ==================================
# DOWNLOAD ERROR EXCEL
# ==================================


@seller_import.route(
    "/excel/errors"
)
def download_errors():


    errors = session.get(
        "excel_errors",
        []
    )


    if not errors:

        flash(
            "Xatolar mavjud emas",
            "info"
        )

        return redirect(
            url_for(
                "seller.products"
            )
        )



    path = create_error_excel(
        errors
    )


    return send_file(
        path,
        as_attachment=True,
        download_name=
        "Excel_import_errors.xlsx",

        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )