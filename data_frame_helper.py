import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def to_snake_case(text):
    s1 = first_cap_re.sub(r'\1_\2', text)
    return all_cap_re.sub(r'\1_\2', s1).lower()

def columns_to_snake_case(data_frame):
    data_frame.columns = [to_snake_case(column) for column in data_frame.columns]
    return data_frame

if __name__ == "__main__":
    print(to_snake_case('TesteDosTesTESTestes'))