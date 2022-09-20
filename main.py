from ctypes.wintypes import RGB
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image,ImageDraw

def display(image,cmap="viridis"):
    plt.imshow(image,cmap=cmap)
    plt.show()

def get_circle_image(image):
    height,width = image.size
    lum_img = Image.new('L', [height,width] , 0) # 2d array of image dims and all values are 0
    #display(np.array(lum_img),"gray")
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height,width)], 0, 360, 
                fill = 255, outline = "white")     # 2d array center filled with white pixel 
    img_arr =np.array(image)
    mask =np.array(lum_img)
    inverse = cv2.bitwise_not(mask)
    output_image=cv2.bitwise_and(img_arr,img_arr,mask=mask)
    output_image=output_image + np.stack((inverse,)*3,axis=-1) # image is still rectangular so filling outside corners with white pixels.
    return output_image

def check(i,j,x,w,r):
    if i<0 or j<0 :
        return False

    if (i-x) ** 2 + (j-w)**2 - r*r <0:
        return True
    else :
        return False


def resize(img1,basew):
    basewidth = basew
    wpercent = (basewidth/float(img1.size[0]))
    hsize = int((float(img1.size[1])*float(wpercent)))
    return img1.resize((basewidth,basewidth), Image.ANTIALIAS)
    


def merge(img,b,h,w):
    #display(img)
    top_x= h - img.shape[0]//2
    top_y= w - img.shape[1]//2
    radius=max(img.shape[0],img.shape[1]) //2
    # print(top_x)
    # print(top_y)
    #mask=np.zeros(back.shape,dtype=np.uint8)
    for i in range(top_x,top_x+img.shape[0]): #b.shape[0]
        for j in range(top_y,top_y+img.shape[1]): #b.shape[1]
            if i<b.shape[0] and j<b.shape[1]:
                if check(i,j,h,w,radius):
                    b[i,j]=img[i-top_x][j-top_y]
 
    return b

    
DIR="./images/"
image_path1=DIR+"person.jpeg"
image_path2=DIR+"person.jpeg"
back_path=DIR+"fil2_back_2.jpg"
output_name="test5.jpg"
img1=Image.open(image_path1).convert("RGB")
img2=Image.open(image_path2).convert("RGB")
back=Image.open(back_path).convert("RGB")

img1 = resize(img1,400)
img2 = resize(img2,400)
back =back.resize((1200,900),Image.ANTIALIAS)
back=np.array(back)
c1 = get_circle_image(img1)
#c2= get_circle_image(img2)
merged = merge(c1,back,227,586)
#merged = merge(c2,merged,300,1000)

display(merged)
#display(back) # here object passes as refference hence back is also got maniplulated

op=Image.fromarray(merged)
op.save("./output_images/filter2_"+output_name)



