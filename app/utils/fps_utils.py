def parse_filter_str(filter_str):
    for op in ['>=', '<=', '>', '<', '=', ' like ', ' ilike ']:
        if op in filter_str:
            field, value = filter_str.split(op, 1)
            return field.strip(), op.strip(), value.strip()
    return None, None, None

def apply_operator(column, op, value):
    if op in ['>=', '<=', '>', '<', '=']:
        value = int(value)
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
    elif op == 'like':
        return column.like(f'%{value}%')
    elif op == 'ilike':
        return column.ilike(f'%{value}%')
    return None