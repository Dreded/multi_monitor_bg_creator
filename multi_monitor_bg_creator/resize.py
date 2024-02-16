import cv2
import numpy as np
import os
import sys


def quit(reason=None):
    sys.exit(reason)


class Resizer:
    def __init__(self, image, desired_resolution, ofilename, multi_save, overwrite):
        self.orig_full_name = image
        self.check_input_image()
        self.orig_image = cv2.imread(image)
        self.orig_name, self.orig_ext = os.path.splitext(image)
        self.orig_height, self.orig_width, _ = self.orig_image.shape
        self.desired_res = desired_resolution
        self.output_res = self.calc_output_res()
        self.monitor_count = len(desired_resolution)
        self.split_images = []
        self.multi_save = multi_save
        self.overwrite = overwrite
        self.ofilename = ofilename

        # probably won't need height but grab it anyhow
        self.max_width = 0
        self.max_height = 0
        for resolution in desired_resolution:
            if resolution[0] > self.max_width:
                self.max_width = resolution[0]
            if resolution[1] > self.max_height:
                self.max_height = resolution[1]

    def check_input_image(self):
        if not os.path.isfile(self.orig_full_name):
            quit("Input image does not exist or is not a file!")
        if not cv2.haveImageReader(self.orig_full_name):
            quit("OpenCV cannot handle this file, is it an image?")

    def split(self):
        height = self.orig_height

        print(
            f"Splitting into {self.monitor_count} images from {self.orig_width} x {self.orig_height}"
        )
        edges = np.linspace(0, self.orig_width, self.monitor_count + 1)
        for start, end in zip(edges[:-1].astype(int), edges[1:].astype(int)):
            self.split_images.append(self.orig_image[0:height, start:end])

    def add_borders(self, resolution, i):
        if resolution[0] < self.max_width:
            # I may be wrong but dont think this would ever be desired
            # here for easy addition in future if needed.
            pass
        if resolution[1] < self.max_height:
            print("\tAdding Border to Height(centered)")
            border_size = int((self.max_height - resolution[1]) / 2)
            border_added = cv2.copyMakeBorder(
                self.split_images[i],
                border_size,
                border_size,
                0,
                0,
                cv2.BORDER_CONSTANT,
            )
            self.split_images[i] = border_added

    def resize(self):
        i = 0
        for resolution in self.desired_res:
            h, w, _ = self.split_images[i].shape
            des_h = resolution[1]
            des_w = resolution[0]
            image_res = [w, h]
            print(f"Image {i}: Desired = {resolution}\t Current = {image_res}")
            if resolution == image_res:
                print("\tDesired resolution already met, adding borders as needed.")
                self.add_borders(resolution, i)

            else:
                print("\tResizing...")
                resized = cv2.resize(self.split_images[i], (des_w, des_h))
                h, w, _ = resized.shape
                image_res = [w, h]
                print(f"\tResized to: {image_res}")
                self.split_images[i] = resized
                self.add_borders(resolution, i)
            i = i + 1

    def wait_or_exit(self):
        while True:
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("q"):
                quit(
                    "Image not saved. Press any-key except 'q' to save on preview window."
                )
            # 255 is no key, this effectively is the elusive any_key
            elif pressedKey != 255:
                break
            if cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()
                quit(
                    "Image not saved. To Save run again and press any key on preview to save."
                )

    def rejoin(self):
        joined = cv2.hconcat(self.split_images)
        cv2.imshow("Output", joined)
        self.joined = joined
        h, w, _ = joined.shape
        self.output_res = [w, h]
        self.wait_or_exit()

    def calc_output_res(self):
        width = 0
        height = 0
        for res in self.desired_res:
            width += res[0]
            if res[1] > height:
                height = res[1]
        return [width, height]

    def suggest_filename(self):
        res = f"{self.output_res[0]}x{self.output_res[1]}"
        ext = self.orig_ext
        name = self.orig_name
        if self.ofilename:
            name = self.ofilename

        filename = f"{name}_{res}{ext}"

        if self.multi_save:
            filenames = []
            for x in range(self.monitor_count):
                filenames.append(filename.replace(ext, f"_{x}{ext}"))
            return filenames

        return [filename]

    def save(self, output_file_name):
        if self.multi_save:
            for x in range(self.monitor_count):
                cv2.imwrite(output_file_name[x], self.split_images[x])
                print(f"Saved to: {output_file_name[x]}")

        else:
            cv2.imwrite(output_file_name[0], self.joined)
            print(f"Saved to: {output_file_name[0]}")

    def set_file_name(self):
        if self.overwrite:
            if self.multi_save:
                quit(
                    "How do you expect to overwrite the original and save to multiple files?"
                )

            print(f"You will be overwriting the image at {self.orig_full_name}")
            print(
                "You will still be able to [q]uit at the image preview without overwrite"
            )
            key = input("Enter 'y' to continue: ")
            if key.upper() != "Y":
                quit("Exiting, Nothing done")
            else:
                return [self.orig_full_name]

        return self.suggest_filename()

    def do_default(self):
        filename = self.set_file_name()
        for file in filename:
            print(f"Filename will be: {file}")

        self.split()
        self.resize()
        self.rejoin()
        self.save(filename)


if __name__ == "__main__":
    os.system("clear")
    print("Not meant to be run standalone.")
