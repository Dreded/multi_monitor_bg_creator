import multi_monitor_bg_creator as resize
import os
import argparse

def split_resolutions(res_list):
    output = []
    for res in res_list:
        item = res.split('x')
        if len(item) != 2:
            raise Exception("Must provide resolution as str or int e.g. '1920x1080' and only 2 numbers per res")
        item[0] = int(item[0])
        item[1] = int(item[1])
        output.append(item)
    return output

def get_args():
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument('image', help="Image to split up")
    parser.add_argument('-mr','--monitor_res', help="Enter in your monitor resolution[s] '1920x1080' multiple -mr for multiple monitors", default=None,action='append')
    parser.add_argument('-o','--output', help="Output filename eg '/tmp/image.jpg'", required=False)
    return parser.parse_args()


os.system("clear")
args = get_args()
if args.monitor_res:
    out_res = split_resolutions(args.monitor_res)
else:
    out_res = [[1920,1080],[2560,1440],[1920,1080]]
r = resize.resize.Resizer(args.image,out_res)
r.do_default(args.output)
