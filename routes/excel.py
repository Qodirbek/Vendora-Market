from flask import Blueprint, send_file
from utils.excel_template import create_product_template


excel = Blueprint(
    "excel",
    __name__,
    url_prefix="/excel"
)



@excel.route(
    "/template"
)
def template():

    file = create_product_template()

    return send_file(
        file,
        as_attachment=True
    )