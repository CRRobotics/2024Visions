import numpy as np

TAG_FAMILY = "tag36h11"
MARGIN_THRESHOLD = 40
DECODE_SHARPENING=.25
REFINE_EDGES=1
QUAD_DECIMATE = 1
QUAD_SIGMA=0
NTHREADS=1
LOG_PATH = "/home/crr/2024Visions/pose_estimation_pyapriltags/log.csv"
ALT_LOG_PATH = "/home/crr/2024Visions/pose_estimation_pyapriltags/log_after_center.csv"


PIXEL_MARGIN = 12

SERVER = "10.6.39.2"

CAMERA_CONSTANTS = {
    0: {
        "matrix":np.array([
        [1.1116882438499686e+03, 0.0, 6.4491686786616367e+02],
        [0.0, 1.1116882438499686e+03, 3.4494788214486431e+02],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            7.1115318392158552e-02,
            -9.0295426044896640e-02,
            0,
            0,
            0
            ]
        ]),
        "yc": -0.04445, #Y coordinate to center of robot. (meters I believe)
        "xc": -0.2667, #X coordinate to center of robot. (meters I believe)
        "thetar": -57, # Rotation to center of robot.
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    2: {
        "matrix":np.array([
        [1.1858734566777853e+03, 0.0, 6.2056335691161883e+02],
        [0.0, 1.1858734566777853e+03, 4.0056159502284038e+02],
        [0.0, 0.0, 1.0]
        ]), 
        "distortion":np.array([
            [
            7.1434391893902743e-02,
            -1.0290634335247859e-01,
            0,
            0,
            3.1899527796588695e-02
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    4: {
        "matrix":np.array([
        [8.3032651252814117e+02, 0.0, 6.3287687153719173e+02],
        [0.0, 8.3032651252814117e+02, 4.2247754245647945e+02],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            -3.4388726691113503e-01,
            1.5036501773752539e-01,
            0,
            0,
            -3.6869412893688829e-02
            ]
        ]),
        "yc": 0.3175,
        "xc": -.2667, #.145 for kitbot, -.105 for duckbot
        "thetar": 0
    },
    6: {
        "matrix":np.array([
        [4.1168382419129812e+03, 0.0, 7.3632272128065506e+02],
        [0.0, 4.1168382419129812e+03, 1.7728661000112291e+02],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            -7.6324824951781362e-02,
            7.2204776231230294e-01,
            -9.2128816474088705e-03,
            8.3758889710313037e-03,
            -9.9056807111481575e+00
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0.32385, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    8: {
        "matrix":np.array([
        [ 1.0680455761239421e+03, 0.0, 6.2711096307896184e+02],
        [0.0,  1.0680455761239421e+03, 4.0111217741787573e+02],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            7.9941477780746895e-02,
            -1.1139485335992444e-01,
            0,
            0,
            5.4311014424915989e-02
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    },
    10: {
        "matrix":np.array([
        [1.1016380458677829e+03, 0.0, 6.1313352015451687e+02],
        [0.0, 1.1016380458677829e+03, 3.9368367276654828e+02],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            7.0891554725855066e-02,
            -9.8322113845617787e-02,
            0,
            0,
            2.0901589583073917e-02
            ]
        ]),
        "yc": 0, #Y coordinate to center of robot. (meters I believe)
        "xc": 0.32885, #X coordinate to center of robot. (meters I believe)
        "thetar": 0 # Rotation to center of robot.
    }
}

# apriltag positions. counter-clockwise (lb, rb, rt, lt). 4 corner coordinates (xyz)
ID_POS = {
    1: np.array([
        [15.1509624, 0.287147, 1.273302],
        [15.0079816, 0.204597, 1.273302],
        [15.0079816, 0.204597, 1.438402],
        [15.1509624, 0.287147, 1.438402],
        #[15.079472, 0.245872, 1.355852]
    ]),
    2: np.array([
        [16.2566244, 0.924941, 1.273302],
        [16.1136436, 0.842391, 1.273302],
        [16.1136436, 0.842391, 1.438402],
        [16.2566244, 0.924941, 1.438402],
        #[16.185134, 0.883666, 1.355852]
    ]),
    3: np.array([
        [16.579342, 5.065268, 1.368552],
        [16.579342, 4.900168, 1.368552],
        [16.579342, 4.900168, 1.533652],
        [16.579342, 5.065268, 1.533652],
        #[16.579342, 4.982718, 1.451102]
    ]),
    4: np.array([
        [16.579342, 5.630418, 1.368552],
        [16.579342, 5.465318, 1.368552],
        [16.579342, 5.465318, 1.533652],
        [16.51320685, 5.597270879, 1.533652],
        #[16.579342, 5.547868, 1.451102]
    ]),
    5: np.array([
        [14.618208, 8.2042, 1.273302],
        [14.783308, 8.2042, 1.273302],
        [14.783308, 8.2042, 1.438402],
        [14.618208, 8.2042, 1.438402],
        #[14.700758, 8.2042, 1.355852]
    ]),
    6: np.array([
        [1.75895, 8.2042, 1.273302],
        [1.92405, 8.2042, 1.273302],
        [1.92405, 8.2042, 1.438402],
        [1.75895, 8.2042, 1.438402],
        #[1.8415, 8.2042, 1.355852]
    ]),
    7: np.array([
        [-0.0381, 5.465318, 1.368552],
        [-0.0381, 5.630418, 1.368552],
        [-0.0381, 5.630418, 1.533652],
        [-0.0381, 5.465318, 1.533652],
        #[-0.0381, 5.547868, 1.451102]
    ]),
    8: np.array([
        [-0.0381, 4.900168, 1.368552],
        [-0.0381, 5.065268, 1.368552],
        [-0.0381, 5.065268, 1.533652],
        [-0.0381, 4.900168, 1.533652],
        #[-0.0381, 4.982718, 1.451102]
    ]),
    9: np.array([
        [0.4275983971, 0.842391, 1.273302],
        [0.2846176029, 0.924941, 1.273302],
        [0.2846176029, 0.924941, 1.438402],
        [0.4275983971, 0.842391, 1.438402],
        #[0.356108, 0.883666, 1.355852]
    ]),
    10: np.array([
        [1.533006397, 0.204597, 1.273302],
        [1.390025603, 0.287147, 1.273302],
        [1.390025603, 0.287147, 1.438402],
        [1.533006397, 0.204597, 1.438402],
        #[1.461516, 0.245872, 1.355852]
    ]),
    11: np.array([
        [11.8332356, 3.671951, 1.23825],
        [11.9762164, 3.754501, 1.23825],
        [11.9762164, 3.754501, 1.40335],
        [11.8332356, 3.671951, 1.40335],
        #[11.904726, 3.713226, 1.3208]
    ]),
    12: np.array([
        [11.9762164, 4.457065, 1.23825],
        [11.8332356, 4.539615, 1.23825],
        [11.8332356, 4.539615, 1.40335],
        [11.9762164, 4.457065, 1.40335],
        #[11.904726, 4.49834, 1.3208]
    ]),
    13: np.array([
        [11.220196, 4.187698, 1.23825],
        [11.220196, 4.022598, 1.23825],
        [11.220196, 4.022598, 1.40335],
        [11.220196, 4.187698, 1.40335],
        #[11.220196, 4.105148, 1.3208]
    ]),
    14: np.array([
        [5.320792, 4.022598, 1.23825],
        [5.320792, 4.187698, 1.23825],
        [5.320792, 4.187698, 1.40335],
        [5.320792, 4.022598, 1.40335],
        #[5.320792, 4.105148, 1.3208]
    ]),
    15: np.array([
        [4.712832397, 4.539615, 1.23825],
        [4.569851603, 4.457065, 1.23825],
        [4.569851603, 4.457065, 1.40335],
        [4.712832397, 4.539615, 1.40335],
        #[4.641342, 4.49834, 1.3208]
    ]),
    16: np.array([
        [4.569851603, 3.754501, 1.23825],
        [4.712832397, 3.671951, 1.23825],
        [4.712832397, 3.671951, 1.40335],
        [4.569851603, 3.754501, 1.40335],
        # [4.641342, 3.713226, 1.3208]
    ])
}

# centered at (0, 0, 0)
ID_TESTING_POS = {
    2: np.array([
        [0, -0.08255, -0.08255],
        [0, 0.08255, -0.08255],
        [0, 0.08255, 0.08255],
        [0, -0.08255, 0.08255],
    ])
}
