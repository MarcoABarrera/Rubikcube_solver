

#rangos hsv
red_hsv1=[[0,130,140],[7,255,255]]
red_hsv2=[[150,130,140],[180,255,255]]
orange_hsv1=[[7,140,100],[15,220,255]]
orange_hsv2=[[7,140,100],[15,220,255]]
white_hsv=[[0,0,150],[180,100,255]]
yellow_hsv=[[20,0,0],[45,250,255]]   
blue_hsv=[[90,170,0],[125,255,255]]
green_hsv=[[50,30,220],[86,255,255]]



import cv2
import numpy as np
cap=cv2.VideoCapture(0)
_,frame=cap.read()
height,width,_=frame.shape


square_size_factor=0.4#cuadro de escaneo
square_x1=int((width-((square_size_factor)*height))/2)#cálculo de esquinas
square_x2=int((width+((square_size_factor)*height))/2)


square_y1=int(((1-square_size_factor)/2)*height)
square_y2=int(((1+square_size_factor)/2)*height)

cube_dimension=square_y2-square_y1#largo y ancho de pixeles


def find_color(h,s,v):#encuentra el color en el rango
    if ((red_hsv1[0][0]<=h<=red_hsv1[1][0]) or (red_hsv2[0][0]<=h<=red_hsv2[1][0])) and (red_hsv1[0][2]<=v<=red_hsv1[1][2]):
        return "r"
    elif ((orange_hsv1[0][0]<=h<=orange_hsv1[1][0]) or (orange_hsv2[0][0]<=h<=orange_hsv2[1][0])) and (orange_hsv1[0][2]<=v<=orange_hsv1[1][2]):
        return "o"
    elif (yellow_hsv[0][0]<=h<=yellow_hsv[1][0]) and (yellow_hsv[0][1]<=s<=yellow_hsv[1][1]):
        return "y"
    elif (green_hsv[0][0]<=h<=green_hsv[1][0]) and (green_hsv[0][1]<=s<=green_hsv[1][1]):
        return "g"
    elif (white_hsv[0][0]<=h<=white_hsv[1][0]) and (white_hsv[0][1]<=s<=white_hsv[1][1]):
        return "w"
    elif (blue_hsv[0][0]<=h<=white_hsv[1][0]) and (blue_hsv[0][1]<=s<=blue_hsv[1][1]):
        return "b"    
    else:
        print("h ",h," s ",s," v ",v,"colour not recognized")


def find_face_colors(face_hsv):#color de cada tile
    face_colors=[]
    for row in face_hsv:
        row_colors=[]
        for tile in row:
            
            row_colors.append(find_color(tile[0],tile[1],tile[2]))
        face_colors.append(row_colors)
    return face_colors



def find_avg_hsv(img):#encuentra los colores de la imagen recortada
        
    tile_dimension=int(cube_dimension/3)#cuadro de 3x3
    tile_factor=0.3#factor of area where colour will be found(tile roi)
    tile_roi_start=int(((1-tile_factor)/2)*tile_dimension)#pixels to start of bounding rectangle of tile roi
    tile_roi_end=int((tile_dimension*tile_factor)+tile_roi_start)#pixels to end of bounding rectangle of tile roi
    
    tile_roi=[]#list which will hold roi (in image form) of all individual tiles
    for j in range(3):
        row=[]
        for i in range(3):
            row.append(img[(j*tile_dimension)+tile_roi_start:(j*tile_dimension)+tile_roi_end,(i*tile_dimension)+tile_roi_start:(i*tile_dimension)+tile_roi_end])#roi finding math
            cv2.rectangle(img, ((i*tile_dimension)+tile_roi_start,(j*tile_dimension)+tile_roi_start), ((i*tile_dimension)+tile_roi_end,(j*tile_dimension)+tile_roi_end), (255,0,0), 1)#draws rectangle on each tile roi
        tile_roi.append(row)
    cv2.imshow("check",img)
    hsv_avg=[]#list which will hold avg hsv value of each tile
    bgr_avg=[]
    h_all=set()
    s_all=set()
    v_all=set()
    for row_iterable in tile_roi:
        row=[]
        bgr_row=[]
        for col_iterable in row_iterable:
            b_avg,g_avg,r_avg,_=np.uint8(cv2.mean(col_iterable))#averages bgr value in roi
            color=cv2.cvtColor(np.uint8([[[b_avg,g_avg,r_avg]]]),cv2.COLOR_BGR2HSV)#converts bgr value to corresponding hsv
            h_avg= color[0][0][0]
            s_avg= color[0][0][1]
            v_avg= color[0][0][2]

            h_all.add(h_avg)
            s_all.add(s_avg)
            v_all.add(v_avg)

            #bgr_row.append([b_avg,g_avg,r_avg])
            row.append([h_avg,s_avg,v_avg])
        hsv_avg.append(row)
    
    #bgr_avg.append(bgr_row)
    print(hsv_avg[0],"\n",hsv_avg[1],"\n",hsv_avg[2])
    
    #print(bgr_avg)
    print("h",min(h_all),max(h_all))
    print("s",min(s_all),max(s_all))
    print("v",min(v_all),max(v_all))
    return hsv_avg

    

while True:
    _,frame=cap.read()
    
    cv2.rectangle(frame, (square_x1, square_y1), (square_x2, square_y2), (255,0,0), 2)#cube should be placed within this square



    cv2.imshow("original",frame)
    k=cv2.waitKey(1) & 0xff
    if k==27:#ESC is pressed
        break
    elif k==32:#SPACE is pressed
        print("Image Captured")
        
        
        cube_roi=frame[square_y1:square_y2,square_x1:square_x2]
        
        
        
        print(find_face_colors(find_avg_hsv(cube_roi)))
    
        print("\n"*2)




cap.release()
cv2.destroyAllWindows()
