import cv2
import numpy as np
import os
import argparse

def main(image_path):
    image = cv2.imread(image_path)
    

    if image is None:
        print("Error: Could not read the image.")
        return

    # Use cv2.aruco.Dictionary_get if your OpenCV version is older than 3.3
    aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_4X4_250)
    aruco_params = cv2.aruco.DetectorParameters()
    corners, ids, rejected = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

    if ids is None or len(ids) < 4:
        print("Error: At least four ArUco markers are required.")
        return
        
    sorted_corners = [corner for _, corner in sorted(zip(ids, corners), key=lambda x: x[0][0])][:4]
    src_points = np.array([corner[0][0] for corner in sorted_corners], dtype=np.float32)
    dst_points=np.array( [[[0., 0.],
        [1070., 0.],
        [1070. ,1070.],
        [0., 1070.]]
        ], dtype=np.float32)
    height, width = image.shape[:2]
    
    
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    transformed_image = cv2.warpPerspective(image, matrix, (width, height))

    gray = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
    
    
    margin = 10
    height, width = gray.shape
    mask = np.zeros_like(gray)
    mask[margin:height-margin, margin:width-margin] = 1

# Apply thresholding with the mask
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.bitwise_and(binary, binary, mask=mask)

# Find contours
    contours1, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
    obstacle_image = transformed_image.copy()
    cv2.drawContours(obstacle_image, contours1, -1, (0, 255, 0), 2)

    total_area = sum(cv2.contourArea(c) for c in contours1)

    output_dir = os.path.dirname(image_path)
    cv2.imwrite(os.path.join(output_dir, 'output_image.jpg'), obstacle_image)

    with open(os.path.join(output_dir, 'obstacles.txt'), 'w') as f:
        f.write(f"Aruco ID: {[id[0] for id in ids]}\n")
        f.write(f"Obstacles: {len(contours1)}\n")
        f.write(f"Area: {total_area}")

    print("Processing complete. Check the output directory for results.")
           
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process image for 2D map creation")
    parser.add_argument("--image", required=True, help="Path to the input image")
    args = parser.parse_args()
    main(args.image)
