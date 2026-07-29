import openpyxl

from extensions import db
from models.product import Product



def import_products(
    file_path,
    seller_id=None
):

    workbook = openpyxl.load_workbook(
        file_path
    )

    sheet = workbook.active


    success = 0
    errors = []


    row_number = 1



    for row in sheet.iter_rows(
        min_row=2,
        values_only=True
    ):

        row_number += 1


        try:

            (
                offer_id,
                sku,
                name,
                description,
                brand,
                price,
                old_price,
                stock,
                image

            ) = row



            # ======================
            # VALIDATION
            # ======================

            if not name:

                raise Exception(
                    "Mahsulot nomi kiritilmagan"
                )


            if not offer_id:

                raise Exception(
                    "Offer ID kiritilmagan"
                )



            # ======================
            # DUPLICATE CHECK
            # ======================

            exists_offer = Product.query.filter_by(
                offer_id=str(offer_id)
            ).first()



            if exists_offer:

                raise Exception(
                    "Bu offer_id mavjud"
                )



            if sku:

                exists_sku = Product.query.filter_by(
                    sku=str(sku)
                ).first()


                if exists_sku:

                    raise Exception(
                        "Bu SKU mavjud"
                    )



            # ======================
            # CREATE PRODUCT
            # ======================


            product = Product(

                offer_id=str(
                    offer_id
                ),


                sku=str(
                    sku
                ) if sku else None,


                name=str(
                    name
                ),


                description=description,


                brand=brand,


                price=int(
                    price or 0
                ),


                old_price=int(
                    old_price or 0
                ),


                stock=int(
                    stock or 0
                ),


                image=image,


                seller_id=seller_id,


                active=False,

                approved=False

            )



            # ======================
            # AUTO FUNCTIONS
            # ======================


            product.calculate_discount()


            product.create_slug()



            db.session.add(
                product
            )


            success += 1



        except Exception as e:


            errors.append(

                {

                    "row": row_number,

                    "data": row,

                    "error": str(e)

                }

            )



    try:

        db.session.commit()


    except Exception as e:


        db.session.rollback()


        errors.append(

            {

                "row": "DATABASE",

                "error": str(e)

            }

        )




    return {

        "success": success,

        "errors": errors,

        "total": success + len(errors)

    }





# ==================================
# ADMIN UCHUN ALIAS
# ==================================


def import_products_from_excel(
    file_path,
    seller_id=None
):

    return import_products(
        file_path,
        seller_id
    )