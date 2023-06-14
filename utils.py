from open_flow import RectangularChannel, TrapezoidalChannel, TriangularChannel, CircularChannel
from sympy import Symbol

definitions = {
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
            'channel_type': 'Section type of Channel',
            'zc': 'Section Factor',
            'yc': 'Critical Depth',
            'Sc': 'Critical Slope',
}

def calculate_section(section_input, n_input, So_input, Q_input=None, b_input=None, z_input=None, D_input= None, y_input = Symbol('y')):
    if section_input == "Rectangle":
        section = RectangularChannel(n_input, So_input, Q_input, b_input, y_input)

    elif section_input == "Triangle":
        section = TriangularChannel(n_input, So_input, Q_input, z_input, y_input)

    elif section_input == "Trapezoid":
        section = TrapezoidalChannel(n_input, So_input, Q_input, b_input, z_input, y_input)

    elif section_input == "Circle":
        section = CircularChannel(n_input, So_input, Q_input, D_input, y_input)
    return section

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

def formater_str(results, selection = None):
    formated_results = ''
    for value in definitions:
        if value in results:
            if selection != None and value not in selection:
                continue
            formated_results += definitions[value]
            result_value = results[value]
            formated_value = trim_decimals(result_value) 
            formated_results += f' = {formated_value}\n'
    return formated_results
