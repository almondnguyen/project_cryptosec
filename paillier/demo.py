import PySimpleGUI as sg

from phe import paillier

# sg.theme_previewer()
sg.theme('DefaultNoMoreNagging')

frame_0 = sg.Frame('You', size=(500, 200), title_location='n', layout=
[
    [
        sg.Button('Generate keys!'),
        sg.Text('', key='=> public_key, private_key')
    ],
    [
        sg.Text('(secret) a  =', size=10, justification='right'), sg.Input(key='a'),
    ],
    [
        sg.Text('(secret) b  =', size=10, justification='right'), sg.Input(key='b'),
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

frame_1 = sg.Frame('Cloud computer', size=(500, 160), title_location='n', layout=
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
        sg.Text('(encrypted + non-encrypted)   \tE(a + c)\t=', key='E(a + c)'),
    ],
    [
        sg.Text('(encrypted * non-encrypted)   \tE(b * c)\t=', key='E(b * c)'),
    ]
])

frame_2 = sg.Frame('You', size=(500, 160), title_location='n', layout=
[
    [
        sg.Text('', key='Receive: E(a + b), E(a + c), E(b * c)'),
    ],
    [
        sg.Button('Decrypt!'),
    ],
    [
        sg.Text('    a + b  \t= ', key='a + b', justification='right'),
    ],
    [
        sg.Text('    a + c  \t= ', key='a + c', justification='right'),
    ],
    [
        sg.Text('    b * c  \t= ', key='b * c', justification='right'),
    ]
]
)

layout = [
    [frame_0],
    [sg.Text('', key='Transfer: E(a), E(b), c')],
    [frame_1],
    [sg.Text('', key='Transfer: E(a + b), E(a + c), E(b * c)')],
    [frame_2]
]

window = sg.Window('Paillier Demo', layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Generate keys!':
        n_length = 2048  # default=2048
        public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)

        window['=> public_key, private_key'].update('=> public_key, private_key')

    elif event == 'Encrypt!':
        a = float(window['a'].get())
        b = float(window['b'].get())
        encr_a = public_key.encrypt(a)
        encr_b = public_key.encrypt(b)

        window['=> E(a), E(b)'].update('=> E(a), E(b)')
        
    elif event == 'Transfer!':
        c = float(window['c'].get())

        window['Transfer: E(a), E(b), c'].update(f'Transfer: E(a), E(b), {c}')
        window['Receive: E(a), E(b), c'].update(f'Receive: E(a), E(b), {c}')
        
    elif event == 'Compute!':
        encr_a_plus_b = encr_a + encr_b
        window['E(a + b)'].update('(encrypted + encrypted)        \tE(a + b)\t= E(a) + E(b)')

        encr_a_plus_c = encr_a + c
        window['E(a + c)'].update(f'(encrypted + non-encrypted)   \tE(a + c)\t= E(a) + {c}')

        encr_b_mult_c = encr_b * c
        window['E(b * c)'].update(f'(encrypted * non-encrypted)   \tE(b * c)\t= E(b) * {c}')

        window['Transfer: E(a + b), E(a + c), E(b * c)'].update('Transfer: E(a + b), E(a + c), E(b * c)')
        window['Receive: E(a + b), E(a + c), E(b * c)'].update('Receive: E(a + b), E(a + c), E(b * c)')

    elif event == 'Decrypt!':
        a_plus_b = private_key.decrypt(encr_a_plus_b)
        window['a + b'].update(f'    a + b  \t=  {a_plus_b}')

        a_plus_c = private_key.decrypt(encr_a_plus_c)
        window['a + c'].update(f'    a + c  \t=  {a_plus_c}')

        b_mult_c = private_key.decrypt(encr_b_mult_c)
        window['b * c'].update(f'    b * c  \t=  {b_mult_c}')

window.close()
