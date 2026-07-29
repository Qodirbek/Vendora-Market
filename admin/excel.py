import os

from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    render_template,
    send_file
)

from werkzeug.utils import secure_filename

from utils.excel_import import import_products_from_excel
from utils.excel_template import create_product_template


excel_admin = Blueprint(
    "excel_admin",
    __name__,
    url_prefix="/admin/products"
)


UPLOAD_FOLDER = "uploads"


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".",1)[1].lower()
        == "xlsx"
    )



# =========================
# ADMIN EXCEL IMPORT
# =========================

@excel_admin.route(
    "/excel",
    methods=["GET","POST"]
)
def excel_import():

    if request.method == "POST":

        file = request.files.get(
            "file"
        )


        if not file:

            flash(
                "Excel fayl tanlang",
                "danger"
            )

            return redirect(
                url_for(
                    "excel_admin.excel_import"
                )
            )



        if not allowed_file(
            file.filename
        ):

            flash(
                "Faqat XLSX fayl",
                "danger"
            )

            return redirect(
                url_for(
                    "excel_admin.excel_import"
                )
            )



        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )


        filename = secure_filename(
            file.filename
        )


        path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        file.save(path)



        result = import_products_from_excel(
            path,
            None
        )


        flash(
            f"{result['success']} ta mahsulot qo'shildi",
            "success"
        )


        return redirect(
            url_for(
                "admin.dashboard"
            )
        )



    return render_template(
        "admin/product_excel.html"
    )



# =========================
# DOWNLOAD TEMPLATE
# =========================

@excel_admin.route(
    "/excel/template"
)
def excel_template():

    file = create_product_template()


    return send_file(
        file,
        as_attachment=True,
        download_name=
        "admin_product_template.xlsx"
    )