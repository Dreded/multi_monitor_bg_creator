import multi_monitor_bg_creator as resize
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument('image', help="Image to split up")
    parser.add_argument('-dr','--desired_resolution', help="An array of the desired resolutions default=[[1920,1080],[2560,1440],[1920,1080]]", required=False, default=[[1920,1080],[2560,1440],[1920,1080]])
    parser.add_argument('-o','--output', help="Output filename with eg /tmp/image.jpg", required=False)
    return parser.parse_args()


os.system("clear")
args = get_args()

r = resize.resize.Resizer(args.image,args.desired_resolution)
r.do_default(args.output)
