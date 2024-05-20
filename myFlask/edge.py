from math import floor
from turtle import width
from flask import Blueprint, jsonify, request
from scipy.ndimage import gaussian_filter
import cv2
import numpy as np
import urllib.request
import base64
from PIL import Image

bp = Blueprint('edge', __name__)

def read_image(img_url):
    req = urllib.request.urlopen(img_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    img = addPadding(img, 0.1)
    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

def addPadding(img, rate):
    width = img.shape[1]
    height = img.shape[0]
    top = np.int16(height*rate)
    left = np.int16(width*rate)
    value = [0, 0, 0]    
    dst = cv2.copyMakeBorder(img, top, top, left, left, cv2.BORDER_CONSTANT, None, value)
    dst = cv2.resize(dst, (width, height))
    return dst

def extract_alpha_channel(img):
    return img[:, :, 3]

def get_largest_contour(alpha_channel, thinkness):
    smoothed = cv2.GaussianBlur(alpha_channel, (thinkness, thinkness),0)
    contours_smoothed = cv2.findContours(smoothed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_smoothed = contours_smoothed[0] if len(contours_smoothed) == 2 else contours_smoothed[1]
    big_contour_smoothed = max(contours_smoothed, key=cv2.contourArea)
    peri = cv2.arcLength(big_contour_smoothed, True)
    return cv2.approxPolyDP(big_contour_smoothed, 0.0001 * peri, True)

def draw_filled_contour_on_black_background(big_contour, shape):
    contour_img = np.zeros(shape)
    cv2.drawContours(contour_img, [big_contour], 0, 255, -1)
    return contour_img

def apply_dilation(img, outLine):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (outLine, outLine))
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

def contours_to_svg(contours):
    svg_paths = []
    for contour in contours:
        path = "M"
        for point in contour:
            path += f"{point[0][0]},{point[0][1]} "
        path += "Z"
        svg_paths.append(path)
    return svg_paths

def douglas_peucker(points, epsilon):
    if len(points) <= 2:
        return points
    d_max = 0
    index = 0
    end = len(points) - 1
    for i in range(1, end):
        d = np.linalg.norm(np.cross(
            np.array(points[i]) - np.array(points[0]), 
            np.array(points[end]) - np.array(points[0])
        )) / np.linalg.norm(np.array(points[end]) - np.array(points[0]))
        if d > d_max:
            index = i
            d_max = d
    if d_max > epsilon:
        rec_results1 = douglas_peucker(points[:index+1], epsilon)
        rec_results2 = douglas_peucker(points[index:], epsilon)
        
        result = rec_results1[:-1] + rec_results2
    else:
        result = [points[0], points[-1]]
    return result

def draw_ellipse_between_points(img, p1, p2, color=(0, 255, 0), thickness=1):
    center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)    
    major_axis = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) // 2
    minor_axis = min(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) // 2
    angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    cv2.ellipse(img, center, (major_axis, minor_axis), angle, 0, 360, color, thickness)
    return img

def smooth_svg_path(path_str, epsilon = 1):
    points_str = path_str.replace("M", "").replace("L", "").replace("Z", "").split()
    points = [tuple(map(float, p.split(','))) for p in points_str]
    return np.array(douglas_peucker(points, epsilon))

@bp.route('/edge', methods=['POST'])
def handle_edge():
    if request.is_json:
        try:
            req = request.json
            image_url, outLine, inLine, contour_type, outLine = req.get("image_url"), req.get("outLine"), req.get("inLine"), req.get("contours_type", "path"), req.get("outLine", 0)
            print(image_url)
            if not image_url.startswith(('http://', 'https://')):
                return jsonify({"error": "Invalid URL"}), 400
            img = read_image(image_url) 
            img_width = img.shape[1]
            img_height = img.shape[0]
            outLine = floor(img_width / 500 * outLine) + ((floor(img_width / 500 * outLine)) + 1)%2
            inLine = floor(img_width / 500 * inLine) + ((floor(img_width / 500 * inLine)) + 1)%2
            kernel = np.ones((inLine, inLine), np.uint8)
            alpha = extract_alpha_channel(img)

            origin_contour = get_largest_contour(alpha, floor(img_width / 500 * 35) + ((floor(img_width / 500 * 35)) + 1)%2)
            origin_img = draw_filled_contour_on_black_background(origin_contour, alpha.shape)
            origin_img = origin_img.astype(np.uint8)
            big_contour = get_largest_contour(origin_img, outLine)

            pp = origin_img.astype(np.uint8)
            image_erode = cv2.erode(pp, kernel)
            
            normal_big_contour = get_largest_contour(image_erode, 1)
            contour_img = draw_filled_contour_on_black_background(big_contour, alpha.shape)

            normal_contour_img = draw_filled_contour_on_black_background(normal_big_contour, alpha.shape)

            if outLine > 0:
                contour_img = apply_dilation(contour_img, outLine)

            if contour_type == 'path':
                image = contour_img.astype(np.uint8)
                origin_image = origin_img.astype(np.uint8)
                normal_image = normal_contour_img.astype(np.uint8)
                contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                origin_contours, _ = cv2.findContours(origin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                normal_contours, _ = cv2.findContours(normal_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
                
                # first = cv2.drawContours(img, normal_contours, 0, (50, 50, 50), 1)
                # second = cv2.drawContours(img, origin_contours, 0, (50, 50, 50), 1)
                # third = cv2.drawContours(img, contours, 0, (50, 50, 50), 1)
                
                # cv2.imwrite('img.jpg', img)
                # cv2.imwrite('img.png', img)

                first = cv2.drawContours(image, normal_contours, 0, (50, 50, 50), 1)
                second = cv2.drawContours(image, origin_contours, 0, (50, 50, 50), 1)
                third = cv2.drawContours(image, contours, 0, (50, 50, 50), 1)
                
                cv2.imwrite('image.jpg', image)
                
                svg_paths = contours_to_svg(contours)
                svg_points = smooth_svg_path(svg_paths[0], 0.8)
                xscipy = gaussian_filter(svg_points[:, 0], 1, mode='wrap')
                yscipy = gaussian_filter(svg_points[:, 1], 1, mode='wrap')
                svg_points = []
                for i in range(0, len(xscipy)-1):
                    svg_points.append([xscipy[i], yscipy[i]])
                # cv2.polylines(img, [np.array(svg_points, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)

                # cv2.imwrite('contour_img.jpg', contour_img)

                bw_image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
                mask = cv2.threshold(bw_image, 127, 255, cv2.THRESH_BINARY_INV)[1]
                image = cv2.cvtColor(bw_image, cv2.COLOR_GRAY2BGRA)
                image[:, :, 3] = cv2.bitwise_not(mask)
                cv2.imwrite('img.png', img)
                cv2.imwrite('image.png', image)
                cv2.imwrite('image.jpg', image)

                # contour_img = cv2.imread('contour_img.png')
                # img = cv2.imread('img.png')

                # result_image = cv2.addWeighted(contour_img, 0.01, img, 1, 0)
                # cv2.imwrite('result_image.jpg', result_image)
                # cv2.imwrite('result_image.png', result_image)
                result_image = Image.open("image.png")
                result_image_jpg = Image.open("image.jpg")
                result_image.info['dpi'] = (300, 300)
                result_image.save('300DPI.png', format="PNG")
                result_image_jpg.save('300DPI.jpg', format="JPEG", dpi=(300, 300))

                # png_image = Image.open('300DPI.png')

                # # Get the DPI information
                # dpi = png_image.info.get('dpi')
                # print("300DPI.png DPI INFO--->", dpi)

                return jsonify({"points": svg_points, "width": img_width, "height": img_height}), 200
            else:
                retval, buffer = cv2.imencode('.png', image)
                image_base64 = base64.b64encode(buffer).decode('utf-8')

                return jsonify({"mask": image_base64}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return "Request was not JSON", 400