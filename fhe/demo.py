import PySimpleGUI as sg
import numpy as np
from Pyfhel import Pyfhel

# sg.theme_previewer()
sg.theme('DefaultNoMoreNagging')

frame_0 = sg.Frame('You', size=(500, 200), title_location='n', layout=
[
    [
        sg.Text('(secret) a  =', size=10, justification='right'), sg.Input(key='a'),
    ],
    [
        sg.Text('(secret) b  =', size=10, justification='right'), sg.Input(key='b'),
    ],
    [
        sg.Button('Generate keys!'),
        sg.Text('', key='=> public_key, private_key')
    ],
    [
        sg.Button('Encrypt!'),
        sg.Text('', key='=> E(a), E(b)')
    ],
    [
        sg.Text('c  =', size=10, justification='right'), sg.Input( key='c'),
    ],
    [
        sg.Button('Transfer!')
    ]
])

frame_1 = sg.Frame('Cloud computer', size=(500, 250), title_location='n', layout=
[
    [  
        sg.Text('', key='Receive: E(a), E(b), c')
    ],
    [
        sg.Button('Compute!', key='Compute!'),
    ],
    [
        sg.Text('(encrypted + encrypted)\t\tE(a + b)\t=', key='E(a + b)'),
    ],
    [
        sg.Text('(encrypted - encrypted)\t\tE(a - b)\t=', key='E(a - b)'),
    ],
    [
        sg.Text('(encrypted + non-encrypted)   \tE(a + c)\t=', key='E(a + c)'),
    ],
    [
        sg.Text('(encrypted - non-encrypted)   \tE(a - c)\t=', key='E(a - c)'),
    ],
    [
        sg.Text('(encrypted * encrypted)       \t\tE(a * b)\t=', key='E(a * b)'),
    ],
    [
        sg.Text('(encrypted * non-encrypted)   \tE(b * c)\t=', key='E(b * c)'),
    ]
])

frame_2 = sg.Frame('You', size=(500, 160), title_location='n', layout=
[
    [
        sg.Text('', key='Receive: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)'),
    ],
    [
        sg.Button('Decrypt!'),
    ],
    [
        sg.Text('    a + b  \t= ', key='a + b', justification='right'),sg.Text('    \ta - b  \t= ', key='a - b', justification='right'),
    ],
    [
        sg.Text('    a + c  \t= ', key='a + c', justification='right'),sg.Text('    \ta - c  \t= ', key='a - c', justification='right'),
    ],
    [
        sg.Text('    a * b  \t= ', key='a * b', justification='right'),sg.Text('    \tb * c  \t= ', key='b * c', justification='right'),
    ]
]
)

layout = [
    [frame_0],
    [sg.Text('', key='Transfer: E(a), E(b), c')],
    [frame_1],
    [sg.Text('', key='Transfer: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)')],
    [frame_2]
]

window = sg.Window('FHE BFV/CKKS Scheme Demo', layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Generate keys!':
        type = ''
        HE = Pyfhel()     
        a = str(window['a'].get())
        b = str(window['b'].get())
        if a.isdigit() and b.isdigit():
            type = 'bfv'
            HE.contextGen(scheme=type, n=2**14, t_bits=20)  # Generate context for 'bfv'/'ckks' scheme
                        # The n defines the number of plaintext slots.
                        #  There are many configurable parameters on this step
                        #  More info in Demo_2, Demo_3, and Pyfhel.contextGen()
            a = np.array([int(a)], dtype=np.int64)
            b= np.array([int(b)], dtype=np.int64)
        elif a.replace('.','',1).isdigit() and b.replace('.','',1).isdigit():
            type = 'CKKS'
            HE.contextGen(scheme = type, n=2**14, scale = 2**30, qi_sizes =  [60, 30, 30, 30, 60])
            a = np.array([float(a)], dtype=np.float64)
            b= np.array([float(b)], dtype=np.float64)
  
        HE.keyGen()             # Key Generation: generates a pair of public/secret keys

        window['=> public_key, private_key'].update('=> public_key, private_key')

    elif event == 'Encrypt!':
        if type == 'bfv':
            encr_a = HE.encryptInt(a) # Encryption makes use of the public key
            encr_b = HE.encryptInt(b) # For integers, encryptInt function is used.
        elif type == 'CKKS':
            ptxt_a = HE.encodeFrac(a)   # Creates a PyPtxt plaintext with the encoded arr_x
            ptxt_b = HE.encodeFrac(b)   # plaintexts created from arrays shorter than 'n' are filled with zeros.
            
            encr_a = HE.encryptPtxt(ptxt_a) # Encrypts the plaintext ptxt_x and returns a PyCtxt
            encr_b = HE.encryptPtxt(ptxt_b) #  Alternatively you can use HE.encryptFrac(arr_y)

        window['=> E(a), E(b)'].update('=> E(a), E(b)')
        
    elif event == 'Transfer!':
        c = float(window['c'].get())

        window['Transfer: E(a), E(b), c'].update(f'Transfer: E(a), E(b), {c}')
        window['Receive: E(a), E(b), c'].update(f'Receive: E(a), E(b), {c}')
        
    elif event == 'Compute!':
        encr_a_plus_b = encr_a + encr_b
        window['E(a + b)'].update('(encrypted + encrypted)        \tE(a + b)\t= E(a) + E(b)')

        encr_a_minus_b = encr_a - encr_b
        window['E(a - b)'].update('(encrypted - encrypted)        \t\tE(a - b)\t= E(a) - E(b)')

        encr_a_plus_c = encr_a + c
        window['E(a + c)'].update(f'(encrypted + non-encrypted)   \tE(a + c)\t= E(a) + {c}')

        encr_a_minus_c = encr_a - c
        window['E(a - c)'].update(f'(encrypted - non-encrypted)        \tE(a - c)\t= E(a) - {c}')

        encr_a_mult_b = encr_a*encr_b
        window['E(a * b)'].update('(encrypted * encrypted)        \t\tE(a * b)\t= E(a) * E(b)')

        encr_b_mult_c = encr_b * c
        window['E(b * c)'].update(f'(encrypted * non-encrypted)   \tE(b * c)\t= E(b) * {c}')

        window['Transfer: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)'].update('Transfer: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)')
        window['Receive: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)'].update('Receive: E(a + b), E(a - b), E(a + c), E(a - c), E(a * b), E(b * c)')

    elif event == 'Decrypt!':
        if type == 'bfv':
            a_plus_b = HE.decryptInt(encr_a_plus_b)[0]
            window['a + b'].update(f'    a + b  \t=  {a_plus_b}')

            a_minus_b = HE.decryptInt(encr_a_minus_b)[0]
            window['a - b'].update(f'    a - b  \t=  {a_minus_b}')

            a_plus_c = HE.decryptInt(encr_a_plus_c)[0]
            window['a + c'].update(f'    a + c  \t=  {a_plus_c}')

            a_minus_c = HE.decryptInt(encr_a_minus_c)[0]
            window['a - c'].update(f'    a - c  \t=  {a_minus_c}')

            a_mult_b = HE.decryptInt(encr_a_mult_b)[0]
            window['a * b'].update(f'    a * b  \t=  {a_mult_b}')

            b_mult_c = HE.decryptInt(encr_b_mult_c)[0]
            window['b * c'].update(f'    b * c  \t=  {b_mult_c}')
        elif type == 'CKKS':
            a_plus_b = HE.decryptFrac(encr_a_plus_b)[0]
            window['a + b'].update(f'    a + b  \t=  {a_plus_b}')

            a_minus_b = HE.decryptFrac(encr_a_minus_b)[0]
            window['a - b'].update(f'    a - b  \t=  {a_minus_b}')

            a_plus_c = HE.decryptFrac(encr_a_plus_c)[0]
            window['a + c'].update(f'    a + c  \t=  {a_plus_c}')

            a_minus_c = HE.decryptFrac(encr_a_minus_c)[0]
            window['a - c'].update(f'    a - c  \t=  {a_minus_c}')

            a_mult_b = HE.decryptFrac(encr_a_mult_b)[0]
            window['a * b'].update(f'    a * b  \t=  {a_mult_b}')

            b_mult_c = HE.decryptFrac(encr_b_mult_c)[0]
            window['b * c'].update(f'    b * c  \t=  {b_mult_c}')

window.close()