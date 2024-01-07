import numpy as np

TAG_FAMILY = "tag16h5"
MARGIN_THRESHOLD = 41
PIXEL_MARGIN = 7

SERVER = "10.6.39.2"

CAMERA_CONSTANTS = {
    1: {
        "matrix":np.array([
        [1097.3387663520302, 0.0, 614.1053531279227],
        [0.0, 1090.798847106442, 429.49732257606695],
        [0.0, 0.0, 1.0]
        ]),
        "distortion":np.array([
            [
            0.11689586201295843,
            -0.5199784733199033,
            -0.0004565757059130622,
            -0.008706649747024026,
            1.0476502704411934
            ]
        ]),
        "yc": 0.04445, #Y coordinate to center of robot. (meters I believe)
        "xc": -0.2667, #X coordinate to center of robot. (meters I believe)
        "thetar": 57 # Rotation to center of robot.
    }
}

##apriltag positions. clockwise. 4 corner coordinates (xyz)
ID_POS = {
    1: np.array([
        [],
        [],
        [],
        []
    ]),
    2: np.array([
        [],
        [],
        [],
        []
    ]),
    3: np.array([
        [],
        [],
        [],
        []
    ]),
    4: np.array([
        [],
        [],
        [],
        []
    ]),
    5: np.array([
        [],
        [],
        [],
        []
    ]),
    6: np.array([
        [],
        [],
        [],
        []
    ]),
    7: np.array([
        [],
        [],
        [],
        []
    ]),
    8: np.array([
        [],
        [],
        [],
        []
    ]),
    9: np.array([
        [],
        [],
        [],
        []
    ]),
    10: np.array([
        [],
        [],
        [],
        []
    ]),
    11: np.array([
        [],
        [],
        [],
        []
    ]),
    12: np.array([
        [],
        [],
        [],
        []
    ]),
    13: np.array([
        [],
        [],
        [],
        []
    ]),
    14: np.array([
        [],
        [],
        [],
        []
    ]),
    15: np.array([
        [],
        [],
        [],
        []
    ])
}