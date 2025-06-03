import pyrealsense2 as rs
import numpy as np
import cv2

# Configure the pipeline
pipeline = rs.pipeline()
config = rs.config()

# Enable color and depth streams
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
profile=pipeline.start(config)
ctx = rs.context()

depth_sensor = profile.get_device().first_depth_sensor()
# High Accuracy preset
if depth_sensor.supports(rs.option.visual_preset):
    depth_sensor.set_option(rs.option.visual_preset, 3)

# Manual exposure
depth_sensor.set_option(rs.option.enable_auto_exposure, 0)
depth_sensor.set_option(rs.option.exposure, 15000)
depth_sensor.set_option(rs.option.gain, 16)
# Use High Accuracy preset if supported
if depth_sensor.supports(rs.option.visual_preset):
    for i in range(6):
        desc = depth_sensor.get_option_value_description(rs.option.visual_preset, i)
        print(f"{i}: {desc}")
    depth_sensor.set_option(rs.option.visual_preset, 3)  # 3 = High Accuracy
try:
    while True:
        # Wait for a coherent set of frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap to depth image for better visualization
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03),
            cv2.COLORMAP_JET
        )

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.imshow('RealSense Color + Depth', images)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
