import cv2
import numpy as np
# import gc
# gc.set_debug(gc.DEBUG_STATS)

class DescriptorExtractor():
    __slots__ = 'size'
    """Classe para extrair keypoints e descritores utilizando a classe Surf do OpenCV."""
    def __init__(self):
        self.size = 0
    def extract(self, img_name, feature_detector_alg=None):
        # Lê imagem
        img = cv2.imread(img_name,0)
        # Testa se imagem é válida
        if not isinstance(img, (np.ndarray)):
            return

        # Livres
        if feature_detector_alg.upper() == 'BRISK':
            des_extract = cv2.BRISK_create(50)
        elif feature_detector_alg.upper() == 'ORB':
            des_extract = cv2.ORB_create(1000)
        elif feature_detector_alg.upper() == 'AKAZE':
            des_extract = cv2.AKAZE_create()
        elif feature_detector_alg.upper() == 'KAZE':
            des_extract = cv2.KAZE_create()
        # Não-livres
        elif feature_detector_alg.upper() == 'SIFT':
            des_extract = cv2.xfeatures2d.SIFT_create(1000)
        elif feature_detector_alg.upper() == 'SURF':
            des_extract = cv2.xfeatures2d.SURF_create(400)
        else:
            raise Exception(" Algorithm not available.")

        # Extrai keypoints e descritores da imagem
        kp , des = des_extract.detectAndCompute(img, None)
        kp.clear()
        img = None
        del kp, img

        # print(des, len(des[0]), type(des), len(des), des.size)

        # Testa se os descritores são válidos
        if not isinstance(des, (np.ndarray)):
            return False
        self.size += len(des)
        return des.tolist()

if __name__ == '__main__':
    d = DescriptorExtractor()
    des = d.extract('../../../../Pictures/dataset100/9', 'surf')
    print(des, len(des))
