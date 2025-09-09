""" Used by DoubleRangeSpatialFacet.valueToQuery """


def int_between_operation(context, row):
    """ plone.app.querystring.operation.int.between """
    values = row.values
    if not values or len(values) != 2:
        return {}

    try:
        min_val, max_val = int(values[0]), int(values[1])
    except (ValueError, TypeError):
        return {}

    catalog = context.portal_catalog
    index = catalog._catalog.indexes.get(row.index)

    if index is None:
        return {}

    all_vals = index._index.keys()
    numeric_vals = [int(v) for v in all_vals if str(v).isdigit()]

    selected = [str(v) for v in numeric_vals if min_val <= v <= max_val]

    return {
        row.index: {
            "query": selected,
        }
    }
