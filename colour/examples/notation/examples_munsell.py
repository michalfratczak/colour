"""Showcase *Munsell Renotation System* computations."""

import numpy as np

import colour
from colour.utilities import message_box

message_box('"Munsell Renotation System" Computations')

Y = 12.23634268
message_box(
    f'Computing "Munsell" value using "Priest, Gibson and MacNicholas (1920)" '
    f'method for given "luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="Priest 1920"))
print(colour.notation.munsell_value_Priest1920(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "Munsell, Sloan and Godlove (1933)" '
    f'method for given "luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="Munsell 1933"))
print(colour.notation.munsell_value_Munsell1933(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "Moon and Spencer (1943)" method for '
    f'given "luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="Moon 1943"))
print(colour.notation.munsell_value_Moon1943(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "Saunderson and Milner (1944)" method '
    f'for given "luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="Saunderson 1944"))
print(colour.notation.munsell_value_Saunderson1944(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "Ladd and Pinney (1955)" method for '
    f'given "luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="Ladd 1955"))
print(colour.notation.munsell_value_Ladd1955(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "McCamy (1987)" method for given '
    f'"luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="McCamy 1987"))
print(colour.notation.munsell_value_McCamy1987(Y))

print("\n")

message_box(
    f'Computing "Munsell" value using "ASTM D1535-08e1" method for given '
    f'"luminance" value:\n\n\t{Y}'
)
print(colour.munsell_value(Y, method="ASTM D1535"))
print(colour.notation.munsell_value_ASTMD1535(Y))

print("\n")

xyY = np.array([0.38736945, 0.35751656, 0.59362000])
message_box(
    f'Converting to the "Munsell" colour from given "CIE xyY" colourspace '
    f"values:\n\n\t{xyY}"
)
print(colour.xyY_to_munsell_colour(xyY))

print("\n")

for munsell_colour in ("4.2YR 8.1/5.3", "N8.9"):
    message_box(
        f'Converting to the "CIE xyY" colourspace from given "Munsell" '
        f"colour:\n\n\t{munsell_colour}"
    )
    print(colour.munsell_colour_to_xyY(munsell_colour))
    print("\n")
