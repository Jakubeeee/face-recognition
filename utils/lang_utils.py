def nvl(nullable_value, replacement):
    if nullable_value is not None:
        return nullable_value
    else:
        return replacement
