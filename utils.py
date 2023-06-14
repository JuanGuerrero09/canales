from open_flow import RectangularChannel, TrapezoidalChannel, TriangularChannel, CircularChannel
from pipe_flow import Pipe
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
            'ID': 'Internal Diameter [m]',
            'e': 'Surface Roughness [m]',
            'eD': 'Relative Roughness',
            'Re': 'Reynolds Number',
            'L': 'Length [m]',
            'method': 'Calculation Type',
            'C': 'Hazen-Williams Coef.',
            'flow_type': 'Flow Regime',
            'fr': 'Darcy Friction Factor',
            'h': 'Loss per meter [m/m]',
            'hf':'Major Loss [m]'
}

'e' 'eD' 'Re' 'L' 'method' 'C' 'flow_type' 'f' 'h' 'hf'

def calculate_section(section_input, n_input, So_input, Q_input=None, b_input=None, z_input=None, D_input= None, y_input = Symbol('y')):
    if section_input == "Rectangle":
        section = RectangularChannel(n=n_input, So=So_input, Q=Q_input, b=b_input, y=y_input)

    elif section_input == "Triangle":
        section = TriangularChannel(n=n_input, So=So_input, Q=Q_input, z=z_input, y=y_input)

    elif section_input == "Trapezoid":
        section = TrapezoidalChannel(n=n_input, So=So_input, Q=Q_input, b=b_input, z=z_input, y=y_input)

    elif section_input == "Circle":
        section = CircularChannel(n=n_input, So=So_input, Q=Q_input, D=D_input, y=y_input)
    return section

def calculate_pipe(calc_type, L_input, ID_input, Q_input, e_input = None, C_input = None):
    if calc_type == 'Darcy-Weisbach':
        pipe = Pipe(Q_input, ID_input, e_input, L_input)
    elif calc_type == 'Hazen-Williams':
        pipe = Pipe(Q_input, ID_input, L = L_input, C= C_input, method= calc_type)
    return pipe

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
        if value in results and results[value] != None:
            if selection != None and value not in selection:
                continue
            formated_results += definitions[value]
            result_value = results[value]
            formated_value = trim_decimals(result_value) 
            formated_results += f' = {formated_value}\n'
    return formated_results
