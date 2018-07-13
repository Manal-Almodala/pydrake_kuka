import os

output_height = 1080
output_width = 1920

n_horizontal_tiles = 3
n_vertical_tiles = 3
tile_width = output_width / n_horizontal_tiles
tile_height = output_height / n_vertical_tiles

n_examples = 9

cmd = "avconv "
for i in range(n_examples):
    cmd += "-i seed_%d.ogg " % (i*1000)

filter_complex_str = "nullsrc=size={w}x{h}:duration=60 [tmp_0]; ".format(
    w=output_width, h=output_height)
for i in range(n_examples):
    wi = i/n_vertical_tiles
    hi = i % n_vertical_tiles
    filter_complex_str += \
        "[{i}:v] setpts=PTS-STARTPTS, scale={w}x{h} [tile_{wi}_{hi}];\n"\
        .format(i=i, w=tile_width, h=tile_height, wi=wi, hi=hi)
    input_name = "[tmp_%d]" % i
    output_name = ""
    if i != n_examples - 1:
        output_name = "[tmp_%d];" % (i + 1)
    filter_complex_str += \
        "{input_name}[tile_{wi}_{hi}] " \
        "overlay=x={w_start}:y={h_start} " \
        "{output_name}\n".format(
            input_name=input_name, w=tile_width, h=tile_height,
            output_name=output_name, wi=wi, hi=hi,
            w_start=tile_width*wi, h_start=tile_height*hi)

cmd += '-filter_complex "%s" ' % filter_complex_str
cmd += "-c:v libx264 output.mkv"
print cmd
os.system(cmd)
