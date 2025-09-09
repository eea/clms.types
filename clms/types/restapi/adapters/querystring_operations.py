# Used by DoubleRangeSpatialFacet.valueToQuery
#
# def int_between_operation(context, field, value):
#     """Custom operation: between two integers (inclusive)."""
#     import pdb
#     pdb.set_trace()
#     if not value or len(value) != 2:
#         return {}
#
#     try:
#         min_val, max_val = int(value[0]), int(value[1])
#     except (TypeError, ValueError):
#         return {}
#
#     return {
#         field: {
#             "query": [min_val, max_val],
#             "range": "min:max",
#         }
#     }

# def int_between_operation(context, field, value):
#     """Custom operation: between two integers (inclusive)."""
#     if not value or len(value) != 2:
#         return {}
#     try:
#         min_val, max_val = int(value[0]), int(value[1])
#     except (ValueError, TypeError):
#         return {}
#
#     return {
#         field: {
#             "query": (min_val, max_val),
#             "range": "min:max"
#         }
#     }

# def int_between_operation(context, field, value):
#     """Test operation: use only min value, ignore max."""
#     import pdb
#     pdb.set_trace()
#     if not value:
#         return {}
#
#     try:
#         min_val = int(value[0])
#     except (ValueError, TypeError, IndexError):
#         return {}
#
#     return {
#         field: {
#             "query": min_val,
#             "range": "min"
#         }
#     }

# def int_between_operation(context, row):
#     """Custom int between query operation.
#
#     row.index  -> index name (example: 'spatial_resolution')
#     row.values -> values sent (example: ['100', '200'])
#     """
#     # import pdb
#     # pdb.set_trace()
#     values = row.values
#
#     if not values or len(values) != 2:
#         return {}
#
#     try:
#         min_val, max_val = int(values[0]), int(values[1])
#     except (ValueError, TypeError):
#         return {}
#
#     return {
#         row.index: {
#             "query": (min_val, max_val),
#             "range": "minmax",  # or minmax?
#         }
#     }


# def int_between_operation(context, row):
#     """Custom int between query operation."""
#
#     values = row.values
#
#     if not values or len(values) != 2:
#         return {}
#
#     try:
#         min_val, max_val = int(values[0]), int(values[1])
#     except (ValueError, TypeError):
#         return {}
#
#     return {
#         row.index: {
#             "query": (min_val, max_val),
#             "range": "min:max",
#         }
#     }


def int_between_operation(context, row):
    # import pdb
    # pdb.set_trace()
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print(row)
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
