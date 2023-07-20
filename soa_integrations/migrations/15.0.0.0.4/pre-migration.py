def migrate(cr, version):
    cr.execute(
        """ UPDATE
            product_template
        SET
            cod_soa = 0
        WHERE
            cod_soa is null
    """)
    cr.execute(
        """ UPDATE
            product_category
        SET
            cod_soa = 0
        WHERE
            cod_soa is null
    """)