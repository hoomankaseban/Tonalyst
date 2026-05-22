from pathlib import Path

import regex as re
import flet as ft

from .theory import cadences, scale_harmonization, scaler, simplifier


LOGO_IMAGE_PATH=Path(__file__).resolve().parent.parent/'assets'/'logo.png'

SCALE_FORM_LABELS={
    '1':'Major',
    '2':'Natural Minor',
    '3':'Harmonic Minor',
    '4':'Melodic Minor',
    '5':'Harmonic Major',
    '6':'Melodic Major',
}

ROOT_NOTE_PATTERN=re.compile(r'^[A-G](#|b)?$')
QUICK_ROOT_NOTES=['C','D','E','F','G','A','B','C#','F#','Bb','Eb','Ab']
ENHARMONIC_ROOT_HINTS={
    'A#':'Bb',
    'B#':'C',
    'Cb':'B',
    'D#':'Eb',
    'E#':'F',
    'Fb':'E',
    'G#':'Ab',
}


def flet_interface(page):
    page.title='Tonalyst'
    page.theme_mode=ft.ThemeMode.LIGHT
    page.bgcolor='#F5F7FA'
    page.padding=0
    page.scroll=ft.ScrollMode.AUTO

    result_area=ft.Column(spacing=18)

    root_field=ft.TextField(
        label='Root note',
        value='C',
        hint_text='C, F#, Bb',
        prefix_icon=ft.Icons.MUSIC_NOTE,
        border_radius=8,
        filled=True,
        fill_color='#FFFFFF',
        on_submit=lambda event: generate_results(),
        col={'xs':12,'md':4},
    )

    form_dropdown=ft.Dropdown(
        label='Scale form',
        value='1',
        options=[
            ft.DropdownOption(key=code,text=f'{code}. {label}')
            for code,label in SCALE_FORM_LABELS.items()
        ],
        leading_icon=ft.Icons.TUNE,
        border_radius=8,
        filled=True,
        fill_color='#FFFFFF',
        col={'xs':12,'md':5},
    )

    def set_root(note):
        root_field.value=note
        root_field.error=None
        generate_results()

    quick_root_row=ft.Row(
        controls=[
            ft.OutlinedButton(
                content=note,
                tooltip=f'Use {note}',
                on_click=lambda event,note=note: set_root(note),
            )
            for note in QUICK_ROOT_NOTES
        ],
        wrap=True,
        spacing=8,
        run_spacing=8,
    )

    def reset_inputs(event=None):
        root_field.value='C'
        root_field.error=None
        form_dropdown.value='1'
        generate_results()

    def generate_results(event=None):
        scale_name=_normalize_root_note(root_field.value)
        form=form_dropdown.value or '1'
        root_field.value=scale_name
        root_field.error=None

        if not ROOT_NOTE_PATTERN.fullmatch(scale_name):
            root_field.error='Use A-G with optional # or b.'
            result_area.controls=[_message_panel(
                'Invalid root note',
                'Examples: C, F#, Bb',
                ft.Icons.ERROR_OUTLINE,
                '#FEF2F2',
                '#991B1B',
            )]
            page.update()
            return

        try:
            result=_build_music_result(scale_name,form)
        except Exception as error:
            result_area.controls=[_message_panel(
                'Could not build that scale',
                _scale_error_message(scale_name,error),
                ft.Icons.ERROR_OUTLINE,
                '#FEF2F2',
                '#991B1B',
            )]
        else:
            result_area.controls=[_result_view(result)]
        page.update()

    input_panel=_panel(
        'Scale Builder',
        ft.Icons.PIANO,
        [
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    root_field,
                    form_dropdown,
                    ft.FilledButton(
                        content='Generate',
                        icon=ft.Icons.PLAY_ARROW,
                        bgcolor='#0F766E',
                        color='#FFFFFF',
                        height=48,
                        on_click=generate_results,
                        col={'xs':12,'md':2},
                    ),
                    ft.OutlinedButton(
                        content='Reset',
                        icon=ft.Icons.REFRESH,
                        height=48,
                        on_click=reset_inputs,
                        col={'xs':12,'md':1},
                    ),
                ],
                spacing=12,
                run_spacing=12,
            ),
            ft.Divider(height=1,color='#E2E8F0'),
            ft.Text('Quick roots',size=12,weight=ft.FontWeight.W_600,color='#64748B'),
            quick_root_row,
        ],
        col=12,
    )

    page.add(
        ft.Container(
            padding=ft.Padding(28,24,28,28),
            content=ft.Column(
                controls=[
                    _app_header(),
                    input_panel,
                    result_area,
                ],
                spacing=18,
            ),
        )
    )
    generate_results()


def _normalize_root_note(value):
    value=value.strip()
    if value=='':
        return ''
    return value[0].upper()+value[1:].replace('B','b')


def _build_music_result(scale_name,form):
    scale_with_distance,scale_notes=scaler(scale_name,form)
    scale_chords=scale_harmonization(scale_with_distance,scale_notes)
    cadence=cadences(scale_name,form)
    simplified_scale,simplified_scale_notes,simplified_scale_chords,simplified_cadence=simplifier(
        scale_with_distance,
        scale_notes,
        scale_chords,
        cadence,
    )
    return {
        'scale_name':scale_name,
        'form':form,
        'form_name':SCALE_FORM_LABELS[form],
        'theoretical':{
            'scale':scale_with_distance,
            'notes':scale_notes,
            'chords':scale_chords,
            'cadences':cadence,
        },
        'practical':{
            'scale':simplified_scale,
            'notes':simplified_scale_notes,
            'chords':simplified_scale_chords,
            'cadences':simplified_cadence,
        },
    }


def _scale_error_message(scale_name,error):
    hint=ENHARMONIC_ROOT_HINTS.get(scale_name)
    if hint:
        return f'The current theory engine could not simplify this spelling. Try {hint} instead of {scale_name}.'
    return f'The current theory engine could not simplify this spelling. Details: {error}'


def _app_header():
    return ft.Container(
        padding=ft.Padding(20,18,20,18),
        bgcolor='#111827',
        border_radius=8,
        content=ft.Row(
            controls=[
                _app_logo(),
                ft.Column(
                    controls=[
                        ft.Text('Tonalyst',size=26,weight=ft.FontWeight.W_800,color='#FFFFFF'),
                        ft.Text('Scale notes, harmonized chords, and cadence patterns',size=13,color='#CBD5E1'),
                    ],
                    spacing=2,
                ),
            ],
            spacing=14,
        ),
    )


def _app_logo():
    if not LOGO_IMAGE_PATH.exists():
        return _fallback_logo()

    return ft.Container(
        width=44,
        height=44,
        border_radius=8,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        alignment=ft.Alignment(0,0),
        content=ft.Image(
            src=LOGO_IMAGE_PATH.read_bytes(),
            fit=ft.BoxFit.CONTAIN,
            error_content=_fallback_logo(),
        ),
    )


def _fallback_logo():
    return ft.Container(
        width=44,
        height=44,
        bgcolor='#F59E0B',
        border_radius=8,
        alignment=ft.Alignment(0,0),
        content=ft.Icon(ft.Icons.LIBRARY_MUSIC,color='#111827',size=26),
    )


def _result_view(result):
    title=f"{result['scale_name']} {result['form_name']}"
    theoretical=result['theoretical']
    practical=result['practical']

    return ft.Column(
        controls=[
            _summary_panel(title,theoretical),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _spelling_panel('Theoretical Spelling',ft.Icons.AUTO_AWESOME,theoretical,'#EEF2FF','#3730A3',{'xs':12,'lg':6}),
                    _spelling_panel('Practical Spelling',ft.Icons.PIANO,practical,'#ECFDF5','#047857',{'xs':12,'lg':6}),
                ],
                spacing=16,
                run_spacing=16,
            ),
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _cadence_panel('Theoretical Cadences',theoretical['cadences'],{'xs':12,'xl':6}),
                    _cadence_panel('Practical Cadences',practical['cadences'],{'xs':12,'xl':6}),
                ],
                spacing=16,
                run_spacing=16,
            ),
        ],
        spacing=18,
    )


def _summary_panel(title,data):
    cadence_count=sum(len(patterns) for patterns in data['cadences'].values())
    return _panel(
        title,
        ft.Icons.TUNE,
        [
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    _stat_tile('Notes',len(data['notes']),'#E0F2FE','#0369A1'),
                    _stat_tile('Chords',len(data['chords']),'#FEF3C7','#92400E'),
                    _stat_tile('Cadence sets',len(data['cadences']),'#FCE7F3','#9D174D'),
                    _stat_tile('Patterns',cadence_count,'#DCFCE7','#166534'),
                ],
                spacing=12,
                run_spacing=12,
            )
        ],
        col=12,
    )


def _spelling_panel(title,icon,data,pill_bg,pill_color,col):
    return _panel(
        title,
        icon,
        [
            _label('Scale Notes'),
            _pill_row(data['notes'],pill_bg,pill_color),
            _label('Triads'),
            _pill_row(data['chords'],'#FFF7ED','#9A3412'),
            _label('Intervals'),
            _distance_table(data['scale']),
        ],
        col=col,
    )


def _cadence_panel(title,cadences,col):
    tiles=[
        _cadence_tile(name,patterns)
        for name,patterns in cadences.items()
    ]
    return _panel(title,ft.Icons.LIBRARY_MUSIC,tiles,col=col)


def _cadence_tile(name,patterns):
    pattern_rows=[
        ft.Container(
            padding=ft.Padding(10,8,10,8),
            bgcolor='#FFFFFF',
            border=_border('#E5E7EB'),
            border_radius=8,
            content=ft.Column(
                controls=[
                    ft.Text(f'Pattern {number}',size=12,weight=ft.FontWeight.W_700,color='#475569'),
                    _pill_row(chords,'#F8FAFC','#0F172A'),
                ],
                spacing=8,
            ),
        )
        for number,chords in patterns.items()
    ]

    return ft.Container(
        bgcolor='#FFFFFF',
        border=_border('#E5E7EB'),
        border_radius=8,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.ExpansionTile(
            title=ft.Text(name,size=14,weight=ft.FontWeight.W_700,color='#0F172A'),
            subtitle=ft.Text(f'{len(patterns)} patterns',size=12,color='#64748B'),
            leading=ft.Icons.KEYBOARD_ARROW_RIGHT,
            tile_padding=ft.Padding(12,0,12,0),
            controls_padding=ft.Padding(12,0,12,12),
            collapsed_bgcolor='#FFFFFF',
            bgcolor='#F8FAFC',
            controls=pattern_rows,
        ),
    )


def _panel(title,icon,controls,col=12):
    return ft.Container(
        col=col,
        padding=ft.Padding(18,16,18,18),
        bgcolor='#FFFFFF',
        border=_border('#DDE4EE'),
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon,color='#0F766E',size=22),
                        ft.Text(title,size=18,weight=ft.FontWeight.W_800,color='#111827'),
                    ],
                    spacing=10,
                ),
                *controls,
            ],
            spacing=14,
        ),
    )


def _message_panel(title,message,icon,bgcolor,color):
    return ft.Container(
        padding=ft.Padding(18,16,18,16),
        bgcolor=bgcolor,
        border=_border('#FCA5A5'),
        border_radius=8,
        content=ft.Row(
            controls=[
                ft.Icon(icon,color=color,size=24),
                ft.Column(
                    controls=[
                        ft.Text(title,size=16,weight=ft.FontWeight.W_800,color=color),
                        ft.Text(message,size=13,color=color),
                    ],
                    spacing=2,
                ),
            ],
            spacing=12,
        ),
    )


def _stat_tile(label,value,bgcolor,color):
    return ft.Container(
        col={'xs':6,'md':3},
        padding=ft.Padding(14,12,14,12),
        bgcolor=bgcolor,
        border_radius=8,
        content=ft.Column(
            controls=[
                ft.Text(str(value),size=24,weight=ft.FontWeight.W_800,color=color),
                ft.Text(label,size=12,weight=ft.FontWeight.W_600,color=color),
            ],
            spacing=2,
        ),
    )


def _label(text):
    return ft.Text(text,size=12,weight=ft.FontWeight.W_700,color='#64748B')


def _pill_row(items,bgcolor,color):
    return ft.Row(
        controls=[
            ft.Container(
                padding=ft.Padding(10,6,10,6),
                bgcolor=bgcolor,
                border_radius=8,
                content=ft.Text(str(item),size=13,weight=ft.FontWeight.W_700,color=color,no_wrap=True),
            )
            for item in items
        ],
        wrap=True,
        spacing=8,
        run_spacing=8,
    )


def _distance_table(scale):
    return ft.DataTable(
        columns=[
            ft.DataColumn('Interval'),
            ft.DataColumn('Distance',numeric=True),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f'{left} - {right}',size=13,color='#0F172A')),
                    ft.DataCell(ft.Text(_distance_label(distance),size=13,color='#0F172A')),
                ]
            )
            for (left,right),distance in scale.items()
        ],
        border=_border('#E5E7EB'),
        border_radius=8,
        heading_row_color='#F8FAFC',
        show_bottom_border=True,
        column_spacing=28,
        horizontal_margin=12,
    )


def _distance_label(distance):
    if isinstance(distance,float) and distance.is_integer():
        return str(int(distance))
    return str(distance)


def _border(color):
    side=ft.BorderSide(1,color)
    return ft.Border(side,side,side,side)


def main():
    ft.run(flet_interface)
