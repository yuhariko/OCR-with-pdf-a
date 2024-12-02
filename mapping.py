import fitz

from base_object import ResultObject
from utils import custom_sort


def mapping_other(boxs, result):
    count_tax = 0
    for idx, box in enumerate(boxs):
        if box[1] == "(Company's name):":
            start = idx
            company_name = ''
            while boxs[start + 1][1] != 'Mã số thuế':
                start += 1
                company_name += boxs[start][1] + " "

            result.company_name = company_name.strip()

        elif box[1] == '(Tax code):':
            count_tax += 1
            if count_tax == 2:
                result.tax_code = boxs[idx + 1][1]

        elif box[1].strip() == '(Total amount):':
            string_value = boxs[idx + 1][1]
            result.total_amount = float(string_value.replace('.', ''))

    return result


def check_next_six_equal(data, start_index=0):
    # Extract the values (assuming they are numeric) from the tuples
    values = [item[0][1] for item in data]

    # Check if we have at least 6 values starting from start_index
    if start_index + 6 <= len(values):
        next_six = values[start_index:start_index + 6]
        # Check the pairwise difference condition
        for i in range(len(next_six)):
            if abs(next_six[start_index] - next_six[i]) > 5:
                return False
        return True
    else:
        return False


def table_mapping(boxs, result):
    table_dict = {
        '(No)': [],
        '(Name of goods and services)': [],
        '(Unit)': [],
        '(Quantity)': [],
        '(Unit price)': [],
        '(Amount)': []
    }

    for idx, box in enumerate(boxs):
        if box[1].strip() == '(No)':
            start = idx + 12
            while True:
                if check_next_six_equal(boxs[start:]):
                    for key in table_dict.keys():
                        value = boxs[start][1]
                        if key in ['(Quantity)', '(Unit price)', '(Amount)']:
                            value = float(value.replace('.', '').replace(',', '.'))
                        table_dict[key].append(value)
                        start += 1
                else:
                    break
    result.table = table_dict
    return result


def extract_text(file_path):
    document = fitz.open(file_path)
    text_with_bboxes = []

    # Iterate through pages and extract text
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text_data = page.get_text("dict")

        # Iterate over blocks of text
        for block in text_data['blocks']:
            if block['type'] == 0:
                for line in block['lines']:
                    for span in line['spans']:
                        bbox = span['bbox']
                        text = span['text']
                        text_with_bboxes.append((bbox, text))

    # Sort using the custom sort function
    text_with_bboxes.sort(key=custom_sort)

    result = ResultObject()
    result = mapping_other(text_with_bboxes, result)
    result = table_mapping(text_with_bboxes, result)

    return result.to_dict()
