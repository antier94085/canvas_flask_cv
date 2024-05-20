import cv2
import numpy as np

# Load the JPEG image
jpg_image = cv2.imread('result_image.jpg')

# Convert the JPEG image to a grayscale image
bw_image = cv2.cvtColor(jpg_image, cv2.COLOR_BGR2GRAY)

# Create a mask for the black portions of the image
mask = cv2.threshold(bw_image, 127, 255, cv2.THRESH_BINARY_INV)[1]

# Create a 4-channel image with a transparent background
image = cv2.cvtColor(jpg_image, cv2.COLOR_BGR2BGRA)

# Set the alpha channel based on the mask (black portions become transparent)
image[:, :, 3] = cv2.bitwise_not(mask)

# Display the resulting image with black portions made transparent
cv2.imwrite('Transparent.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()