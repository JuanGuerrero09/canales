import xlsxwriter
from open_flow import TrapezoidalChannel



data = TrapezoidalChannel(n=0.013, So=0.0075, Q=3.5, b=2, z=1.5).__dict__

definition = {
            'n': "Manning's Coef.",
            'So': 'Channel Slope [m/m]',
            'Q': 'Flow Rate [m3/s]',
            'y': 'Depth [m]',
            'b': 'Bottom Width [m]',
            'z': 'Side Slope',
            'D': 'Diameter [m]',
            'a': 'Area [m2]',
            'rh': 'Hydraulic Radius',
            'dh': 'Hydraulic Depth',
            'tw': 'Top Width [m]',
            'p': 'Wetted Perimeter [m]',
            'f': 'Froude Number',
            'v': 'Velocity [m/s]',
            'flow_status': 'Flow Status',
            'zc': 'Section Factor',
            'yc': 'WIP',
            'vc': 'WIP',
        }

def trim_decimals(value):
    result_value = str(value)
    decimal_index = result_value.find(".")
    if decimal_index != -1:
        decimals = len(result_value) - decimal_index - 1
    else:
        decimals = 0
    if decimals and int(decimals) > 4:
        return f'{value:.2f}'
    else:
        return value

def formater_str(results):
    formated_results = ''
    for value in definition:
        if value in results:
            formated_results += definition[value]
            result_value = results[value]
            formated_value = trim_decimals(result_value) 
            formated_results += f' = {formated_value}\n'
    return formated_results


formater_str(data)
disable = {
            'Rectangle': ['z', 'D'],
            'Triangle': ['D', 'b'],
            'Trapezoid': ['D'],
            'Circle': ['z', 'b'],
        }

input = ['b, z, D,']



calc = 'Q'
# objeto de resultados, yn / q, tipo de canal

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

# definition = frozenset(definition.items())

for key in data:
    initial_row = row
    if key in parameters:
        worksheet.write(row, col, key, bold)
        worksheet.write(row, col + 1, trim_decimals(data[key]))
        worksheet.write(row, col + 2, definition[key], ital)
        row += 1  
    final_row = row



row+=1

worksheet.merge_range(row, col, row, col + 2, 'Results',title_format)

row+=1

# worksheet.insert_image('E2', './logo.png')

for key in data:
    if key not in parameters:
        worksheet.write(row, col, key, bold)
        worksheet.write(row, col + 1, trim_decimals(data[key]))
        worksheet.write(row, col + 2, definition[key], ital)
        row += 1 

worksheet.print_area(0,0, row, col + 1)

workbook.close()