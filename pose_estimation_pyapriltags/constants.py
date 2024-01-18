import numpy as np

TAG_FAMILY = "tag36h11"
MARGIN_THRESHOLD = 40
DECODE_SHARPENING=.25
REFINE_EDGES=1
QUAD_DECIMATE = 1
QUAD_SIGMA=0
NTHREADS=1


PIXEL_MARGIN = 7

SERVER = "10.6.39.2"

CAMERA_CONSTANTS = {
    0: {
        "matrix":np.array([
        [1062.4294070176832, 0.0, 659.24877589952052],
        [0.0, 1062.4294070176832, 369.33219087336823],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            .055656123864839833,
            0,
            0,
            0,
            -.11025598404280015
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    2: {
        "matrix":np.array([
        [1056.7997734244436, 0.0, 630.87407868060438],
        [0.0, 1056.7997734244436, 421.30564581242407],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            0.0071127134351176777,
            -0.12054203331230241,
            0,
            0,
            0.0071234992522144713
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    4: {
        "matrix":np.array([
        [6254.9725146650326, 0.0, 530.51506885862818],
        [0.0, 6254.9725146650326, 370.79989006526603],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            -12.307616865384897,
            234.27807348788966,
            0,
            0,
            -3382.3506940723159
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    6: {
        "matrix":np.array([
        [1135.3824875157502, 0.0, 636.54371424379406],
        [0.0, 1135.3824875157502, 429.76526535317402],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            .085351855261617510,
            -.13424455518051401,
            0,
            0,
            .064126046739839987
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