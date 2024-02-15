import cv2
import numpy as np
import os

class Resizer():
    def __init__(self,image,desired_resolution):
        self.orig_image = cv2.imread(image)
        self.orig_name, self.orig_ext = os.path.splitext(image)
        self.orig_height, self.orig_width, _ = self.orig_image.shape
        self.desired_res = desired_resolution
        self.output_res = [0,0]
        self.monitor_count = len(desired_resolution)
        self.split_images = []

        #probably won't need height but grab it anyhow
        self.max_width = 0
        self.max_height = 0
        for resolution in desired_resolution:
            if resolution[0] > self.max_width: self.max_width = resolution[0]
            if resolution[1] > self.max_height: self.max_height = resolution[1]

    def split(self):
        height = self.orig_height

        print(f"Splitting into {self.monitor_count} images from {self.orig_width} x {self.orig_height}")
        edges = np.linspace(0,self.orig_width, self.monitor_count+1)
        for start,end in zip(edges[:-1].astype(int), edges[1:].astype(int)):
            self.split_images.append(self.orig_image[0:height, start:end])

    def add_borders(self,resolution,i):
        if resolution[0] < self.max_width:
            # I may be wrong but dont think this would ever be desired
            # here for easy addition in future if needed.
            pass

        if resolution[1] < self.max_height:
            print("\tAdding Border to Height(centered)")
            border_size = int((self.max_height - resolution[1])/2)
            border_added = cv2.copyMakeBorder(self.split_images[i],border_size,border_size,0,0,cv2.BORDER_CONSTANT)
            self.split_images[i] = border_added


    def resize(self):
        i = 0
        for resolution in self.desired_res:
            h,w,_ = self.split_images[i].shape
            des_h = resolution[1]
            des_w = resolution[0]
            image_res = [w,h]
            print(f"Image {i}: Desired = {resolution}\t Current = {image_res}")
            if resolution == image_res:
                print("\tDesired resolution already met, adding borders as needed.")
                self.add_borders(resolution,i)

            else:
                print("\tResizing...")
                resized = cv2.resize(self.split_images[i], (des_w,des_h))
                h,w,_ = resized.shape
                image_res = [w,h]
                print(f"\tResized to: {image_res}")
                self.split_images[i] = resized
                self.add_borders(resolution,i)
            i = i+1

    def rejoin(self):
        joined = cv2.hconcat(self.split_images)
        cv2.imshow("Output", joined)
        self.joined = joined
        h,w,_ = joined.shape
        self.output_res = [w,h]
        cv2.waitKey(0)

    def suggest_filename(self):
        res = f"{self.output_res[0]}x{self.output_res[1]}"
        ext = self.orig_ext
        name = self.orig_name
        return f"{name}_{res}{ext}"

    def save(self, output_file_name):
        cv2.imwrite(output_file_name, self.joined)

    def do_default(self,ofilename=None):
        self.split()
        self.resize()
        self.rejoin()
        if not ofilename:
            output_file_name = self.suggest_filename()
        else:
            output_file_name = ofilename
        self.save(output_file_name)

if __name__ == "__main__":
    os.system("clear")
    image = "image.jpg"
    desired_resolution = [[1920,1080],
                          [2560,1440],
                          [1920,1080]]
    resize = Resizer(image,desired_resolution)
    resize.do_default()
