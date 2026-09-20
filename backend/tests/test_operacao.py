from app.utils.operacao import servico_compativel_com_area


def test_area_configuravel_compativel_com_categoria_do_servico():
    assert servico_compativel_com_area("ESTETICA", "ESTETICA") is True
    assert servico_compativel_com_area("ESTETICA", "SALAO") is False
    assert servico_compativel_com_area("ESTETICA", None) is True
