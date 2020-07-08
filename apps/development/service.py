from apps.basedata.models import Material, MaterialCategory

from .models import Formula, FormulaDetail, FormulaMeta


def add_formula(data: dict, status: str = "OFFICIAL"):
    """添加配方至数据库"""
    formula_name = iso_name(data["name"])

    formula = Formula(
        name=formula_name,
        version=data["version"],
        status=status,
        processing_way="MAKE",
    )

    if data['created_at']:
        formula.created_at = data['created_at']

    formula.save()

    formula_add_materials(formula, data['materials'])
    formula_add_materials(formula, data['extend_materials'])

    formula_add_metas(formula, data['metas'])
    formula_add_metas(formula, data['technologies'])


def formula_add_metas(formula, metas: dict):
    """
    给配方批量添加 Metas
    :param formula:
    :param metas:
    :return:
    """
    for meta_name, meta_value in metas.items():
        if isinstance(meta_value, list):
            meta_value = ';'.join(meta_value)

        FormulaMeta.objects.create(
            formula=formula,
            name=meta_name,
            value=meta_value,
        )


def formula_add_materials(formula, materials: list):
    """
    给配方批量添加材料
    :param formula:
    :param materials:
    :return:
    """
    category = MaterialCategory.objects.get(code="material")
    for material_data in materials:
        material_name = iso_name(material_data['name'])

        material, _ = Material.objects.get_or_create(
            code=material_name,
            defaults={
                "code": material_name,
                "name": material_name,
                "category": category,
            }
        )

        FormulaDetail.objects.create(
            formula=formula,
            material=material,
            workshop=material_data['workshop'],
            value_type="NUM",
            value=material_data['amount'],
            measure=material_data['unit'],
        )


def iso_name(name):
    return name.replace(' ', '').replace('（', '(').replace('）', ')')
