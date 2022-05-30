def validate_body(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False, field
    return True, None