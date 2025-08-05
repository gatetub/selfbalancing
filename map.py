import argparse
import cv2  # Import OpenCV library for image processing
import imutils
from cv2 import aruco

def detect_aruco_markers(image):
    # Load the ARUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)  # Assuming  DICT_6X6_250

    # Detect ARUco markers in the image
    corners, ids, _ = cv2.aruco.detectMarkers(image, aruco_dict)

    return corners, ids
    
def main():
    # Parse arguments
    print(cv2.__version__)
    parser = argparse.ArgumentParser(description="Process an image for detection.")
    parser.add_argument("--image", type=str, required=True,
                        help="Path to the image file for processing.")
    args = parser.parse_args()

    # Access the image path
    image_path = args.image

    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    # Display the image using OpenCV
    corners, ids = detect_aruco_markers(image)

    # Store the output in a text file
    with open('aruco_output.txt', 'w') as f:
      for i in range(len(ids)):
        marker_id = ids[i][0]  # Get the marker ID
        marker_corners = corners[i][0]  # Get the marker corners
        f.write(f"Marker ID: {marker_id}\n")
        f.write(f"Corner Points: {marker_corners}\n\n")

# Display the image
    cv2.imshow('ARUco Markers', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
