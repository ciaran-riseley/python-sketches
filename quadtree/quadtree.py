import numpy as np
from PIL import Image
import cv2
import argparse




class Quadnode:
    def __init__(self, img, tol=70):
        # compute the average of the image
        M = img.shape[1]//2
        N = img.shape[0]//2
        H = img.shape[0]
        W = img.shape[1]
        
        mean = int(np.floor(np.mean(img)))
        mean_r = int(np.floor(np.mean(img[:,:,0])))
        mean_g = int(np.floor(np.mean(img[:,:,1])))
        mean_b = int(np.floor(np.mean(img[:,:,2])))

        avg_img_r = mean_r*np.ones((H,W), dtype=np.uint8)
        avg_img_g = mean_g*np.ones((H,W), dtype=np.uint8)
        avg_img_b = mean_b*np.ones((H,W), dtype=np.uint8)
        
        MSE_R = np.mean(np.square(np.subtract(img[:,:,0],avg_img_r)))
        MSE_G = np.mean(np.square(np.subtract(img[:,:,1],avg_img_g)))
        MSE_B = np.mean(np.square(np.subtract(img[:,:,2],avg_img_b)))
        MSE = MSE_R + MSE_G + MSE_B
        #print(f"MSE_R shape: {avg_img_r.shape}")

        if (M<2 or N<2) or (MSE < tol):
            self.img = np.stack([avg_img_b, avg_img_g, avg_img_r],axis=2)
            self.nw = None 
            self.ne = None 
            self.sw = None 
            self.se = None
        else:
            #print(f"M,N:{M},{N}")
            nw = img[:N,:M]
            sw = img[N:,:M]
            ne = img[:N,M:]
            se = img[N:,M:]

            self.nw = Quadnode(nw,tol=tol)
            self.ne = Quadnode(ne,tol=tol)
            self.sw = Quadnode(sw,tol=tol)
            self.se = Quadnode(se,tol=tol)
            self.img = None 

    def get_image(self):
        if self.img is not None:
            return self.img
        else:
            child_nw = self.nw.get_image()
            child_sw = self.sw.get_image()
            child_ne = self.ne.get_image()
            child_se = self.se.get_image()
            return np.hstack((np.vstack((child_nw,child_sw)),np.vstack((child_ne,child_se))))

if __name__=="__main__":

    parser = argparse.ArgumentParser(
                    prog='Image quadtree generator',
                    description='Given an image, produces a quadtree representation of the image')
    parser.add_argument("filename")
    parser.add_argument("-t","--tolerance",type=int,help="Threshold for accepting a quad or subdividing further")
    args = parser.parse_args()
    pilimg = Image.open(args.filename)
    img = np.asarray(pilimg)
    print(f"Img shape: {img.shape}, range: {img.min()}-{img.max()}, type: {img.dtype}")
    root_node = Quadnode(img,tol=args.tolerance)
    final_img = root_node.get_image()
    print(f"Final img shape: {final_img.shape}")
    cv2.imshow("b luhhh",final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()