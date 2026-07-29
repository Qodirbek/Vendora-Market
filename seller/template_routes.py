from flask import (
    Blueprint,
    send_file,
    session
)

from utils.excel_template import create_product_template


template = Blueprint(
    "seller_template",
    __name__,
    url_prefix="/seller/products"
)


@template.route("/template")
def product_template():

    seller_id = session.get(
        "seller_id"
    )


    file_path = create_product_template(
        seller_id
    )


    return send_file(
        file_path,
        as_attachment=True,
        download_name="Sotuv_Biznes_Product_Template.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )