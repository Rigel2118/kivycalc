def format_number(num):
    s = str(float(num))
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s
