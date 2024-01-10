import numpy as np

TAG_FAMILY = "tag16h5"
MARGIN_THRESHOLD = 41
PIXEL_MARGIN = 7

SERVER = "10.6.39.2"

CAMERA_CONSTANTS = {
    1: {
        "matrix":np.array([
        [697.44966690936860, 0.0, 325.23918869505667],
        [0.0, 697.44966690936860, 697.44966690936860],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            0.11744612537697446,
            -0.29928725586362032,
            0,
            0,
            -0.21377372818194756
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    }
}

##apriltag positions. counter-clockwise (lb, rb, rt, lt). 4 corner coordinates (xyz)
ID_POS = {
    1: np.array([
        [15.1509624, 0.287147, 1.273302],
        [15.0079816, 0.204597, 1.273302],
        [15.0079816, 0.204597, 1.438402],
        [15.1509624, 0.287147, 1.438402]
    ]),
    2: np.array([
        [16.2566244, 0.924941, 1.273302],
        [16.1136436, 0.842391, 1.273302],
        [16.1136436, 0.842391, 1.438402],
        [16.2566244, 0.924941, 1.438402]
    ]),
    3: np.array([
        [16.579342, 5.065268, 1.368552],
        [16.579342, 4.900168, 1.368552],
        [16.579342, 4.900168, 1.533652],
        [16.579342, 5.065268, 1.533652]
    ]),
    4: np.array([
        [16.579342, 5.630418, 1.368552],
        [16.579342, 5.465318, 1.368552],
        [16.579342, 5.465318, 1.533652],
        [16.51320685, 5.597270879, 1.533652]
    ]),
    5: np.array([
        [14.618208, 8.2042, 1.273302],
        [14.783308, 8.2042, 1.273302],
        [14.783308, 8.2042, 1.438402],
        [14.618208, 8.2042, 1.438402]
    ]),
    6: np.array([
        [1.75895, 8.2042, 1.273302],
        [1.92405, 8.2042, 1.273302],
        [1.92405, 8.2042, 1.438402],
        [1.75895, 8.2042, 1.438402]
    ]),
    7: np.array([
        [-0.0381, 5.465318, 1.368552],
        [-0.0381, 5.630418, 1.368552],
        [-0.0381, 5.630418, 1.533652],
        [-0.0381, 5.465318, 1.533652]
    ]),
    8: np.array([
        [-0.0381, 4.900168, 1.368552],
        [-0.0381, 5.065268, 1.368552],
        [-0.0381, 5.065268, 1.533652],
        [-0.0381, 4.900168, 1.533652]
    ]),
    9: np.array([
        [0.4275983971, 0.842391, 1.273302],
        [0.2846176029, 0.924941, 1.273302],
        [0.2846176029, 0.924941, 1.438402],
        [0.4275983971, 0.842391, 1.438402]
    ]),
    10: np.array([
        [1.533006397, 0.204597, 1.273302],
        [1.390025603, 0.287147, 1.273302],
        [1.390025603, 0.287147, 1.438402],
        [1.533006397, 0.204597, 1.438402]
    ]),
    11: np.array([
        [11.8332356, 3.671951, 1.23825],
        [11.9762164, 3.754501, 1.23825],
        [11.9762164, 3.754501, 1.40335],
        [11.8332356, 3.671951, 1.40335]
    ]),
    12: np.array([
        [11.9762164, 4.457065, 1.23825],
        [11.8332356, 4.539615, 1.23825],
        [11.8332356, 4.539615, 1.40335],
        [11.9762164, 4.457065, 1.40335]
    ]),
    13: np.array([
        [11.220196, 4.187698, 1.23825],
        [11.220196, 4.022598, 1.23825],
        [11.220196, 4.022598, 1.40335],
        [11.220196, 4.187698, 1.40335]
    ]),
    14: np.array([
        [5.320792, 4.022598, 1.23825],
        [5.320792, 4.187698, 1.23825],
        [5.320792, 4.187698, 1.40335],
        [5.320792, 4.022598, 1.40335]
    ]),
    15: np.array([
        [4.712832397, 4.539615, 1.23825],
        [4.569851603, 4.457065, 1.23825],
        [4.569851603, 4.457065, 1.40335],
        [4.712832397, 4.539615, 1.40335]
    ]),
    16: np.array([
        [4.569851603, 3.754501, 1.23825],
        [4.712832397, 3.671951, 1.23825],
        [4.712832397, 3.671951, 1.40335],
        [4.569851603, 3.754501, 1.40335]
    ])
}