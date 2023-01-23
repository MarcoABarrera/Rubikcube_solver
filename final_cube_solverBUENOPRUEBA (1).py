"""VALORES HSV

Varian mucho con la iluminación


"""


#rangos del modo [[min_h,min_s,min_v],[max_h,max_s,max_v]]
red_hsv1=[[0,130,140],[5,255,255]]
red_hsv2=[[150,130,140],[180,255,255]]
orange_hsv1=[[5,100,100],[15,220,255]]
orange_hsv2=[[5,100,100],[15,220,255]]
white_hsv=[[0,0,150],[180,100,255]]
yellow_hsv=[[20,0,0],[45,250,255]]   
blue_hsv=[[90,150,0],[125,255,255]]
green_hsv=[[50,30,220],[86,255,255]]




import time
import serial



import kociemba
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
_,frame=cap.read()
height,width,_=frame.shape


square_size_factor=0.5#fracción de la altura que ocupa el cuadrado
square_x1=int((width-((square_size_factor)*height))/2)#calculo de esquinas cuadrado
square_x2=int((width+((square_size_factor)*height))/2)


square_y1=int(((1-square_size_factor)/2)*height)
square_y2=int(((1+square_size_factor)/2)*height)

cube_dimension=square_y2-square_y1#altura y anchura del cubo en pixeles

cube=[]
def find_color(h,s,v):#encuentra el color tomando los valores hsv (promedio)
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
        print("h ",h," s ",s," v ",v,"color no reconocido")


def find_face_colors(face_hsv):#encuentra el color de cada tile y forma un arreglo 2d de la cara
    face_colors=[]
    for row in face_hsv:
        row_colors=[]
        for tile in row:
            
            row_colors.append(find_color(tile[0],tile[1],tile[2]))
        face_colors.append(row_colors)
    return face_colors



def find_avg_hsv(img):#con la imagen recortada de las caras del cubo encuentra el color de cada tile con base hsv y forma un arreglo 3d
        
    tile_dimension=int(cube_dimension/3)#ya que el cubo tiene 9(3x3) tiles
    tile_factor=0.3#factor del área donde el color puede ser encontrado (tile roi)
    tile_roi_start=int(((1-tile_factor)/2)*tile_dimension)#a partir de que pixel contar
    tile_roi_end=int((tile_dimension*tile_factor)+tile_roi_start)#pixeles finales
    
    tile_roi=[]#list which will hold roi (in image form) of all individual tiles
    for j in range(3):
        row=[]
        for i in range(3):
            row.append(img[(j*tile_dimension)+tile_roi_start:(j*tile_dimension)+tile_roi_end,(i*tile_dimension)+tile_roi_start:(i*tile_dimension)+tile_roi_end])#roi finding math
            cv2.rectangle(img, ((i*tile_dimension)+tile_roi_start,(j*tile_dimension)+tile_roi_start), ((i*tile_dimension)+tile_roi_end,(j*tile_dimension)+tile_roi_end), (255,0,0), 1)#dibuja un cuadradito en cada tile para representar área de cada color
        tile_roi.append(row)
    cv2.imshow("check",img)
    hsv_avg=[]#list which will hold avg hsv value of each tile
    #bgr_avg=[]
    #h_all=set()
    #s_all=set()
    #v_all=set()
    for row_iterable in tile_roi:
        row=[]
        bgr_row=[]
        for col_iterable in row_iterable:
            b_avg,g_avg,r_avg,_=np.uint8(cv2.mean(col_iterable))#valores rgb promedio en la fila
            color=cv2.cvtColor(np.uint8([[[b_avg,g_avg,r_avg]]]),cv2.COLOR_BGR2HSV)#convierte valores rgb a valores hsv
            h_avg= color[0][0][0]
            s_avg= color[0][0][1]
            v_avg= color[0][0][2]

            #h_all.add(h_avg)
            #s_all.add(s_avg)
            #v_all.add(v_avg)

            #bgr_row.append([b_avg,g_avg,r_avg])
            row.append([h_avg,s_avg,v_avg])
        hsv_avg.append(row)
    print(hsv_avg)
    return hsv_avg
        #bgr_avg.append(bgr_row)
    #print(hsv_avg)
    
    #print(bgr_avg)
    #print("h",min(h_all),max(h_all))
    #print("s",min(s_all),max(s_all))
    #print("v",min(v_all),max(v_all))
    
def sol(input1):
	input2=[[[]],[[]],[[]],[[]],[[]],[[]]]

	for i in range(6):
		if(input1[i][1][1]=='y'):
			input2[0]=input1[i]
			break

	for i in range(6):   
		if(input1[i][1][1]=='o'):
			input2[1]=input1[i]
			break

	for i in range(6):
		if(input1[i][1][1]=='g'):
			input2[2]=input1[i]
			break

	for i in range(6):
		if(input1[i][1][1]=='w'):
			input2[3]=input1[i]
			break


	for i in range(6):
		if(input1[i][1][1]=='r'):
			input2[4]=input1[i]
			break




	for i in range(6):
		if(input1[i][1][1]=='b'):
			input2[5]=input1[i]
			break

	for i in range(6):
		for j in range(3):
			for k in range(3):
				if (input2[i][j][k]=='y'):
					input2[i][j][k]='U'
				elif (input2[i][j][k]=='w'):
					input2[i][j][k]='D'
				elif (input2[i][j][k]=='o'):
					input2[i][j][k]='R'
				elif (input2[i][j][k]=='r'):
					input2[i][j][k]='L'
				elif (input2[i][j][k]=='g'):
					input2[i][j][k]='F'
				elif(input2[i][j][k]=='b'):
					input2[i][j][k]='B'

	b=''
	for i in range(6):
		for j in range(3):
			for k in range(3):
				b+=input2[i][j][k]
	
       
	a = kociemba.solve(b)
	print(a)
	
	a = a.replace("U'","R L F2 B2 R' L' D' R L F2 B2 R' L'")
	a = a.replace("U2","R L F2 B2 R' L' D2 R L F2 B2 R' L'")
	a = a.replace("U","R L F2 B2 R' L' D R L F2 B2 R' L'")


	
	return a

def cleansolution(solution):
    cleanedsolution=""
    prev=solution[0]
    for current in solution[1:]:
        if current=="'":
            cleanedsolution+=prev.lower()
        elif current=="2":
            cleanedsolution+=prev
            cleanedsolution+=prev
        else:
            cleanedsolution+=prev
        prev=current
    cleanedsolution+=solution[len(solution)-1]
    cleanedsolution = cleanedsolution.replace("'", "")
    cleanedsolution = cleanedsolution.replace("2", "")
    cleanedsolution = cleanedsolution.replace(" ", "")
    
    return cleanedsolution

def sendarduino(solution):
    ser = serial.Serial('COM3', 9600,timeout=None) #Establece la conexión con el puerto arduino
    time.sleep(1)
    count=0
    for char in solution:
        ser.write(char.encode())
        time.sleep(1)
        #count+=1
        #if count==60:
        #    time.sleep(60)#CHANGE SLEEP TIME ACCORDING TO DELAY BETWEEN MOTORS
        #    count=0

while True:
    _,frame=cap.read()
    
    cv2.rectangle(frame, (square_x1, square_y1), (square_x2, square_y2), (255,0,0), 2)#cara del cubo puesta en este cuadro



    cv2.imshow("original",frame)
    k=cv2.waitKey(1) & 0xff
    if k==27:#ESC presionado
        break
    elif k==32:#Espacio presionado
        print("Imagen capturada")
        
        
        cube_roi=frame[square_y1:square_y2,square_x1:square_x2]#imagen del cubo solo
        
        cubeface=find_face_colors(find_avg_hsv(cube_roi))
        cube.append(cubeface)
        print("Cara escaneada",cubeface)
        print("cube",cube)
        

    elif k==ord('s'):
        #cube = [[['g', 'o', 'o'], ['w', 'y', 'g'], ['y', 'b', 'b']], [['r', 'o', 'o'], ['w', 'g', 'b'], ['b', 'y', 'y']], [['o', 'g', 'r'], ['w', 'w', 'g'], ['w', 'o', 'r']], [['w', 'w', 'o'], ['y', 'b', 'b'], ['b', 'y', 'r']], [['y', 'b', 'b'], ['r', 'r', 'r'], ['g', 'g', 'y']], [['w', 'r', 'g'], ['y', 'o', 'r'], ['g', 'o', 'w']]]
        solution=cleansolution(sol(cube))
        print(solution)
        print(len(solution))
        sendarduino(solution)

    elif k==ord('r'):
        cube.pop()



cap.release()
cv2.destroyAllWindows()
