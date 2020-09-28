
def clean_worksheet(sheet: str, worksheet: str):
    pass

def loop_generator(list, begin_row_number=1):
    for row_number, value in enumerate(list, 1):
        if row_number < begin_row_number:
            continue
        yield value
