import numpy as np

class Reader:
    def Read(self, path: str):
        x, y, z = np.fromfile(path, count=3, dtype=np.int32)
        array = np.fromfile(path, count=x*y*z, offset=24, dtype=np.int16)
        return (x, y, z), array
