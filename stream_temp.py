import streamlit as st
from PIL import Image,ImageDraw
import cv2
from io import BytesIO
import numpy as np

# st.write("Hello World Streamlit.")



# uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])

#selection = st.number_input('Choose a number from 1 to 100:',
# min_value = 0, max_value = 100, value = 50, step = 1)
# st.write('The current number is ', selection)


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

row1 = st.container()
row2 = st.container()

with row1: 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Front image")
        file_front = st.file_uploader("Front image", type=['jpg','png','jpeg'])
        front_width = st.number_input('resize input image',
min_value = 0, max_value = 1000, value = 400, step = 10)
        
    with col2:
        st.subheader("Back image")
        file_back = st.file_uploader("Background image", type=['jpg','png','jpeg'])
        back_width = st.number_input('enter resize width',
min_value = 0, max_value = 3000, value = 1200, step = 100)
        back_height = st.number_input('enter resize height',
min_value = 0, max_value = 2000, value = 900, step = 100)
        
def load(image):
    buf = BytesIO()
    image.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    btn = st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="output.png",
        mime="image/jpeg",
        )




with row2:
    st.subheader("Output")
    x=st.number_input("enter x cordinate",min_value = 0, max_value = 3000, value=0, step = 100)
    y=st.number_input("enter y cordinate",min_value=0,max_value=2000,value=0,step=100)
    if file_front != None and file_back!=None:
        front = Image.open(file_front)
        back = Image.open(file_back)
        print(back_width)
        img1 = resize(front,front_width)
        back =back.resize((back_width,back_height),Image.ANTIALIAS)
        back=np.array(back)
        c1 = get_circle_image(img1)
        # st.image(Image.fromarray(c1))
        # st.write("coordinates are ",x,y)
        merged = merge(c1,back,y,x)
        op=Image.fromarray(merged)
        st.image(op)
        load(op)


#######################################################3


###########################################################3