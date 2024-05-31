#:kivy 2.3.0

<SpaceDesktop>:
    MDLabel:
        text: "U LOH"
    BoxLayout:
        md_bg_color: app.theme_cls.surfaceColor
        size_hint: 1, 1
        Button:
            #style: "elevated"
            text: "filled"
            pos_hint: {"center_x": .5, "center_y": .5}
            md_bg_color: 0,0,0,0
            on_release: root.btn1_callback()