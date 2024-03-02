def parse_filter_str(filter_str):
    for op in ['>=', '<=', '>', '<', '=']:
        if op in filter_str:
            field, value = filter_str.split(op)
            return field, op, value
    return None, None, None

# Placeholder for safely applying operators to construct a query condition
def apply_operator(column, op, value):
    value=int(value)
    if op == '>=':
        return column >= value
    elif op == '<=':
        return column <= value
    elif op == '<':
        return column < value
    elif op == '>':
        return column > value
    elif op == '=':
        return column == value
    # Add more operator mappings as needed
    return None