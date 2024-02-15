import multi_monitor_bg_creator as resize
import os
import sys
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
    parser.add_argument('-mr','--monitor_res', help="Enter in your monitor resolution[s] '1920x1080' multiple -mr for multiple monitors default = '-mr 1920x1080 -mr 2560x1440 -mr 1920x1080'", default=None,action='append')
    parser.add_argument('-o','--output', help="Output filename eg '/tmp/image.jpg' (not for use with -m)", required=False)
    parser.add_argument('-m','--multi_save', help="Save each split image to its own file.", action='store_true')
    args = parser.parse_args()
    #Don't allow custom name and multi-file save.(later TODO)
    if ((args.output != None) and (args.multi_save == True)):
        sys.exit("Can't do custom name with multi-save")
    return args


os.system("clear")
args = get_args()
if args.monitor_res:
    out_res = split_resolutions(args.monitor_res)
else:
    out_res = [[1920,1080],[2560,1440],[1920,1080]]
r = resize.resize.Resizer(args.image,out_res,args.multi_save)
r.do_default(args.output)
