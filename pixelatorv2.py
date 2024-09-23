import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2

def main(file_name1, file_name2):
    # Open images
    im_s = Image.open(file_name1)
    im_b = Image.open(file_name2)
    file_tobe_saved = "pixelator_view_v2.png"

    # Ensure both images are in RGB format before conversion to LAB
    im_s_rgb = ensure_rgb(im_s)
    im_b_rgb = ensure_rgb(im_b)

    # ----------- Original Pixelator Calculation (RGB based) --------------------
    img_s_list = []
    img_b_list = []
    img_s_score = 0
    img_b_score = 0
    
    for pixel in iter(im_s_rgb.getdata()):
        int_val = getIfromRGB(pixel)
        img_s_list.append(int_val)
        img_s_score += int_val % 255

    for pixel in iter(im_b_rgb.getdata()):
        int_val = getIfromRGB(pixel)
        img_b_list.append(int_val)
        img_b_score += int_val % 255

    # Calculate pixel-wise difference in RGB space
    rgb_diff_list = []
    count = 0
    for pixel in img_s_list:
        diff = (img_b_list[count] - pixel) % 255  # Just get the modulo of 255
        rgb_diff_list.append(diff)
        count += 1

    rgb_added = sum(rgb_diff_list)
    pixelator_val_rgb = rgb_added / (im_s.width + im_s.height)
    print('Pixelator RGB value: ', pixelator_val_rgb)

    # ----------- LAB Color Space Difference Calculation -----------------------
    # Convert images to LAB color space for perceptual difference calculation
    im_s_lab = cv2.cvtColor(np.array(im_s_rgb), cv2.COLOR_RGB2LAB)
    im_b_lab = cv2.cvtColor(np.array(im_b_rgb), cv2.COLOR_RGB2LAB)

    lab_diff_list = []
    img_s_score_lab = 0
    img_b_score_lab = 0

    for pixel in iter(im_s_lab.reshape(-1, 3)):
        int_val = np.linalg.norm(pixel)  # Perceptual difference in LAB space
        img_s_score_lab += int_val

    for pixel in iter(im_b_lab.reshape(-1, 3)):
        int_val = np.linalg.norm(pixel)  # Perceptual difference in LAB space
        img_b_score_lab += int_val

    count = 0
    for pixel in im_s_lab.reshape(-1, 3):
        diff = np.linalg.norm(im_b_lab.reshape(-1, 3)[count] - pixel)  # Absolute difference in LAB space
        lab_diff_list.append(diff)
        count += 1

    lab_added = sum(lab_diff_list)
    pixelator_val_lab = lab_added / (im_s.width + im_s.height)
    print('Pixelator LAB value: ', pixelator_val_lab)

    # ----------- Combine RGB and LAB differences -----------------------------
    combined_pixelator_val = pixelator_val_rgb + pixelator_val_lab
    print('Pixelator value: ', combined_pixelator_val)

    # ----------- Calculate Image Difference -----------------------------------
    if img_s_score != 0.0:
        percent_diff_rgb = ((img_s_score / (im_s.width + im_s.height)) - pixelator_val_rgb) / (img_s_score / (im_s.width + im_s.height))
        percent_diff_lab = ((img_s_score_lab / (im_s.width + im_s.height)) - pixelator_val_lab) / (img_s_score_lab / (im_s.width + im_s.height))

        print('Total RGB Image Score: ', (img_s_score / (im_s.width + im_s.height)))
        print('RGB Image Difference: ', (100.0 - percent_diff_rgb * 100))
        print('Total LAB Image Score: ', (img_s_score_lab / (im_s.width + im_s.height)))
        print('LAB Image Difference: ', (100.0 - percent_diff_lab * 100))
    else:
        print('Total Image Score: ', img_s_score)
        print('Image Difference: ', img_s_score * 100)

    # ----------- Create a Difference Matrix for Visualization -----------------
    combined_diff_list = np.add(rgb_diff_list, lab_diff_list)
    diff_matrix = np.array(combined_diff_list).reshape((im_s.height, im_s.width))

    # Apply Sobel filter to detect structural changes
    sobelx = cv2.Sobel(diff_matrix, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(diff_matrix, cv2.CV_64F, 0, 1, ksize=5)
    sobel_combined = np.hypot(sobelx, sobely)

    # Display the differences using a visual plot
    print('[i] CREATING COMBINED PIXELATOR VIEW')
    plt.figure()
    plot_matrix(sobel_combined, combined_pixelator_val)
    plt.savefig(file_tobe_saved)
    plt.show()

def plot_matrix(cm, pixelator_val, cmap='coolwarm'):
    """
    Plot the difference matrix with colormap and display the combined Pixelator value in the title.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(f'Pixelator View v2 (Pixelator value: {pixelator_val:.10f})')
    plt.colorbar()
    plt.tight_layout()

def ensure_rgb(image):
    """
    Convert an image to RGB if it is grayscale.
    """
    if image.mode != 'RGB':
        print(f"Converting image from {image.mode} to RGB.")
        return image.convert('RGB')
    return image

def getIfromRGB(rgb):
    """
    Convert RGB tuple to an integer representation.
    """
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red << 16) + (green << 8) + blue
    return RGBint

if __name__ == '__main__':
    import sys
    import os.path
    args1 = False
    args2 = False
    try:
        args1 = sys.argv[1]
        args2 = sys.argv[2]
        print("Smaller image file: " + args1)
        print("\nLarger image file: " + args2)
        print("\nFinding the Pixelator value between " + args1 + " and " + args2 + ":\n")
    except IndexError:
        print('Error: No file selected!\nPlease, select the files first.\n')
        sys.exit(1)

    if args1 and args2:
        file_name1 = str(args1)
        file_name2 = str(args2)
        is_file1 = os.path.isfile(file_name1)
        is_file2 = os.path.isfile(file_name2)
        if not is_file1 or not is_file2:
            print('\nError: Wrong file selected! Please, check the path and file name again.\n')
            sys.exit(1)
        main(file_name1, file_name2)