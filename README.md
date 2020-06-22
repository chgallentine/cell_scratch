# Cell Scratch Measurement Aid

### Helper program for measuring width of cut in cell scratch experiments

## Change Image Thresholds

A gradient is created, performing some edge detection on the image loaded. This allows for the cut to be visualized. Changing this threshold using the slider changes the division between white and black pixels, adding or decreasing the clarity of image features

## Change Cut-Width Sensitivity

Cut width is measured using the presense of black pixels bordered by white pixels on the image. This slider changes the minimum width of black pixels which is to be considerd. This allows measurement of the cut, ignoring features in the center of the scratch. At a width of zero, any black pixels will be measured as the scratch.

## Toggle Visibility

Pressing 't' (lowercase T) will toggle the view between the threshold view and the cut-width view. In the threshold view, the thresholded image can be viewed. The threshold slider affects this view.

In the cut-width view, the currently selected widths of the cut are visible. These are overlaid on the original image.

## Toggle Measurements

Pressing 'd' (lowercase D) will toggle an overlay showing the width and area of the measured scratch in pixels relative to the original image. The image is resized for use to dimensions 960x540. The shown dimensions are not scaled to this, they are in terms of the original image.