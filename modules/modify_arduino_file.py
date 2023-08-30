from .generate_zM_sending_code import generate_zM_sending_code
from .generate_zM_LCD_text_code import generate_zM_LCD_text_code


def modify_arduino_file(file_path, data):
    zM_texts_list = data['zM_texts']
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    number_of_texts_line_index = None
    zM_on_LCD_start_index = None
    zM_on_LCD_end_index = None
    zM_start_index = None
    zM_end_index = None

    for i, line in enumerate(lines):
        if "// marker of number_of_interiorSign_texts" in line:
            number_of_texts_line_index = i + 1
            lines[number_of_texts_line_index] = f'#define number_of_interiorSign_texts {len(zM_texts_list)}\n'
            

    for i, line in enumerate(lines):
        if "// start | zM text info on LCD" in line:
            zM_on_LCD_start_index = i + 1
        elif "// end | zM text info on LCD" in line:
            zM_on_LCD_end_index = i
            lines[zM_on_LCD_start_index:zM_on_LCD_end_index] = generate_zM_LCD_text_code(zM_texts_list, 12)
            

    for i, line in enumerate(lines):
        if "// start of the zM command sending" in line:
            zM_start_index = i + 1
        elif "// end of the zM command sending" in line:
            zM_end_index = i
            lines[zM_start_index:zM_end_index] = generate_zM_sending_code(zM_texts_list, 12)



    if number_of_texts_line_index is not None and zM_on_LCD_start_index is not None and zM_on_LCD_end_index is not None and zM_start_index is not None and zM_end_index is not None:
        # Write the modified lines back to the .ino file
        with open(file_path, 'w',  encoding='utf-8') as file:
            file.writelines(lines)

        print(f'File {file_path} was successfully updated')

        return "success"
    else:
        print("Couldn't locate marker comments. \n")
        print('number_of_texts_line_index: ', number_of_texts_line_index)
        print('zM_on_LCD_start_index: ', zM_on_LCD_start_index)
        print('zM_on_LCD_end_index: ', zM_on_LCD_end_index)
        print('zM_start_index: ', zM_start_index)
        print('zM_end_index: ', zM_end_index)