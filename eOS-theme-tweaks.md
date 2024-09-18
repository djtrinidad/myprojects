Adjustments to Theme

** These look good with Dark Mode enabled
*** Set Wingpanel Transparency
Create ~/.config/gtk-3.0/gtk.css
.panel.maximized {
    background-color: rgba(0,0,0,0.4);
}

*** Set Plank Transparency (Most are stock settings)
Create Theme folder under ~/.local/share/plank/themes/ThemeName
In that folder copy /usr/share/plank/themes/Matte/dock.theme to the above directory
Ctrl + Right click in Plank, select Preferences
Select your theme
then open then dock.theme file to edit

[PlankTheme]
#The roundness of the top corners.
TopRoundness=10
#The roundness of the bottom corners.
BottomRoundness=10
#The thickness (in pixels) of lines drawn.
LineWidth=1
#The color (RGBA) of the outer stroke.
OuterStrokeColor=0;;0;;0;;0
#The starting color (RGBA) of the fill gradient.
FillStartColor=0;;0;;0;;110
#The ending color (RGBA) of the fill gradient.
FillEndColor=0;;0;;0;;110
#The color (RGBA) of the inner stroke.  (Try at 230 also, and 30)
InnerStrokeColor=0;;0;;0;;0
