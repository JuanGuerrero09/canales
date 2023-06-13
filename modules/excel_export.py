import xlsxwriter
from utils import definitions, trim_decimals
from PIL import Image
import os



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

    worksheet.set_column('B:B', 10, cell_format=cells_format)
    worksheet.set_column('C:C', 15, cell_format=cells_format)
    worksheet.set_column('D:D', 25, cell_format=cells_format)
    worksheet.merge_range('B1:D1', 'Channel Report',title_format)
    worksheet.set_row(0, 40)


    row += 1

    worksheet.merge_range(row, col, row, col + 2, 'Parameters',title_format)


    row += 1

    parameters = ['n', 'So', 'Q', 'b', 'y', 'z', 'D']

    results = ['a', 'p','rh','tw','dh','zc', 'v', 'yc', 'vc', 'channel_type', 'flow_status', 'f', ]

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
    worksheet.set_row(row, 150, cell_format=cells_format)
    worksheet.insert_image(row, col, 'channel.png')
    row+=1

    worksheet.print_area(0,0, row, col + 1)

    workbook.close()

    os.system("start EXCEL.EXE ChannelReport.xlsx")

