from flask import (
    Blueprint,
    send_file
)

from utils.excel_template import create_product_template


product_excel_admin = Blueprint(
    "product_excel_admin",
    __name__,
    url_prefix="/admin/products"
)


@product_excel_admin.route(
    "/excel/template"
)
def excel_template():

    file = create_product_template()


    return send_file(
        file,
        as_attachment=True,
        download_name="product_template.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )