import xlsxwriter
from utils import definitions, trim_decimals
from PIL import Image
import os

data = {'n': 0.013, 'So': 0.0075, 'Q': 3.5, 'y': 0.531804201497051, 'a': 1.06360840299410, 'p': 3.06360840299410, 'rh': 0.347175050817404, 'tw': 2, 'dh': 0.531804201497051, 'zc': 0.775635435373953, 'v': 3.29068479540718, 'f': 
1.44070777128165, 'flow_status': 'Supercritical', 'yn': 0.678373743218602, 'ac': 1.35674748643720, 'rc': 0.404185150035588, 'pc': 3.35674748643720, 'twc': 2, 'yc': 0.678373743218602, 'vc': None, 'sc': 0.00376343371245344, 'channel_type': 'Rectangular', 'b': 2} 

def generate_report(data):

    workbook = xlsxwriter.Workbook('ChannelReport.xlsx')
    worksheet = workbook.add_worksheet('Data')

    worksheet.set_paper(9)
    worksheet.center_horizontally()
    worksheet.set_header('&CHello')


    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    ital = workbook.add_format({'italic': True})
    # Add a number format for cells with money.
    # number_format = workbook.add_format({'num_format': '#,##'})
    # Adjust the column width.
    # Create a format to use in the merged range.
    title_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "fg_color": "#CCFFFF",
        }
    )

    cells_format = workbook.add_format(
        {
            
            "align": "center",
            "valign": "vcenter",
        }
    )

    group_format = workbook.add_format(
        {
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )

    row = 1
    col = 1

    worksheet.set_column('B:B', 20, cell_format=cells_format)
    worksheet.set_column('C:C', 20, cell_format=cells_format)
    worksheet.set_column('D:D', 25, cell_format=cells_format)
    worksheet.merge_range('B1:D1', 'Channel Report',title_format)
    worksheet.set_row(0, 40)


    row += 1

    worksheet.merge_range(row, col, row, col + 2, 'Parameters',title_format)


    row += 1

    parameters = ['n', 'So', 'Q', 'b', 'y', 'z', 'D']

    results = ['a', 'p','rh','tw','dh','zc', 'v', 'yc', 'Sc', 'channel_type', 'flow_status', 'f', ]

    # definitions = frozenset(definitions.items())

    for key in data:
        initial_row = row
        if key in parameters:
            worksheet.write(row, col, key, bold)
            worksheet.write(row, col + 1, trim_decimals(data[key]))
            worksheet.write(row, col + 2, definitions[key], ital)
            row += 1  
        final_row = row



    row+=1
    worksheet.merge_range(row, col, row, col + 2, 'Results',title_format)

    row+=1


    # worksheet.insert_image('E2', './logo.png')

    for key in data:
        if key in results:
            worksheet.write(row, col, key, bold)
            worksheet.write(row, col + 1, trim_decimals(data[key]))
            worksheet.write(row, col + 2, definitions[key], ital)
            row += 1 

    image = Image.open('channel.png')
    image.resize((50, 50))
    image.save('channel.png')
    worksheet.set_row(row, 150)
    worksheet.merge_range(row, col, row, col + 2, 'Results', cells_format)
    worksheet.insert_image(row, col, 'channel.png', {'x_offset': 60, 'y_offset': 15})
    row+=1

    worksheet.print_area(0,0, row, col + 1)

    workbook.close()

    os.system("start EXCEL.EXE ChannelReport.xlsx")
