from PIL import Image
out = Image.new("RGB", (1920, 1080), 'white')
im = []
for i in range(1, 37):
    im.append(Image.open("out/out-{:02d}.png".format(i)))

frame_div = 4
slow_start = 480*3

for frame in range(0, (17280+slow_start)/frame_div):
    for i in range(0, len(im)):
        offX = i*480-frame*frame_div+slow_start
        rest = offX % 480
        offX = offX-rest
        t = rest / 480.0
        # print(t, rest, 480 * t*t*t)
        rest = 480.0 * t*t*t
        offX = offX + int(rest)
        if 1920 > offX > -480:
            out.paste(im[i], (offX,0))
    # out.resize((1280, 720)).save("video/frame-{:05d}.png".format(frame), 'png')
    out.save("video/frame-{:05d}.png".format(frame), 'png')