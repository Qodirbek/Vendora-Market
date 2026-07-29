import openpyxl
from openpyxl.styles import Font
import os


def create_error_excel(errors):

    folder = "uploads/errors"

    os.makedirs(
        folder,
        exist_ok=True
    )


    path = os.path.join(
        folder,
        "import_errors.xlsx"
    )


    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Xatolar"



    sheet.append(
        [
            "Qator",
            "Xato",
            "Ma'lumot"
        ]
    )


    for cell in sheet[1]:

        cell.font = Font(
            bold=True
        )



    for error in errors:

        sheet.append(
            [
                error.get(
                    "row"
                ),

                error.get(
                    "error"
                ),

                str(
                    error.get(
                        "data"
                    )
                )
            ]
        )



    workbook.save(
        path
    )


    return path