ROTATION=$(xsetwacom get "Wacom HID 4846 Finger touch" Rotate)
if [ $ROTATION == none ]; then
	xrandr -o 2
	xinput set-prop "Wacom HID 4846 Finger touch" "Coordinate Transform Matrix" -1 0 1 0 -1 1 0 0 1
else
	xrandr -o 0
	xinput set-prop "Wacom HID 4846 Finger touch" "Coordinate Transform Matrix" 1 0 0 0 1 0 0 0 1
fi

