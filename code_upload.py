# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Tkinter import *
import Tkinter as ttk
from PIL import Image,ImageTk
import time
import os,os.path
import threading
from threading import Timer
import serial.tools.list_ports




path = os.path.dirname(os.path.realpath(__file__))
hex_address = {
  'bride' : str(path +'/hex_files/bride_v1.hex')
}


def load_all_images(size_x,size_y):
  global lcd_image,mainboard_image,bride_image

  lcd_image = ImageTk.PhotoImage(Image.open(str(path + '/images/lcd.png'))
    .resize((size_x, size_y),Image.ANTIALIAS))

  mainboard_image = ImageTk.PhotoImage(Image.open(str(path + '/images/mainboard.png'))
    .resize((size_x, size_y),Image.ANTIALIAS))


  bride_image = ImageTk.PhotoImage(Image.open(str(path + '/images/bride.png'))
    .resize((size_x, size_y),Image.ANTIALIAS))




def on_closing():
  print('bye-bye')
  tk.destroy()




def create_btn(image,pos_x,pos_y,function):
  btn = page.create_image(pos_x, pos_y, image=image, anchor=NW)
  page.tag_bind(btn, "<Button-1>", function)

def clear_page():
  page.delete("all")
  page.create_image(0, 0,anchor=NW, image=background_image)











def main_page(event):
  clear_page()
  create_btn(lcd_image,100,100,lcd_page)
  create_btn(mainboard_image,400,100,mainboard_page)








def lcd_page(event):
  clear_page()


def mainboard_page(event):
  clear_page()
  create_btn(bride_image,100,100,bride_page)



def bride_page(event):
  clear_page()
  
  # time.sleep(0.5)
  upload_arduino_code('bride')












def create_msg_box(image):
  message_box = Canvas(tk,width=screen_width/3, height=screen_height/3)
  message_box.pack()
  message_box.place(x=(screen_width/2-screen_width/6),y=(screen_height/2-screen_height/6))
  message_box.create_image(0, 0,anchor=NW, image=image)
  return message_box

def _destroy_msgbox(msg_box):
  msg_box.destroy()

def destroy_msgbox(msg_box,time):
  threading.Timer(time, _destroy_msgbox,args=(msg_box,)).start()


def upload_cmd(port,machine):
  os.system('/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P'
  +str(port)+' -b115200 -D -Uflash:w:'
  +str(hex_address[machine])+':i')


def upload_arduino_code(machine):
  try:
    
    port = [tuple(p) for p in list(serial.tools.list_ports.comports())][0][0]
    
    if(port.find('AMA') != -1):
      raise 'no port found'
    
    # show uploading message
    message_box = create_msg_box(uploading_image)
    
    x = threading.Thread(target=upload_cmd, args=(port,machine,))
    x.start()
    
    # destrou uploading message
    # destroy_msgbox(message_box,0)

    message_box = create_msg_box(uploaddone_image)
    destroy_msgbox(message_box,3)    
  
  except Exception as e:
    print('error in upload arduino',e)

    message_box = create_msg_box(upfail_image)
    destroy_msgbox(message_box,3) 
  

  main_page(None)










if __name__ == '__main__':
  tk = Tk()
  tk.attributes("-fullscreen", True)

  tk.protocol("WM_DELETE_WINDOW", on_closing)



  screen_height = tk.winfo_screenheight()
  screen_width = tk.winfo_screenwidth()

  x_scaled=(screen_width/40)
  y_scaled=(screen_height/20)

  background_image = ImageTk.PhotoImage(Image.open(str(path + '/images/background.png'))
    .resize((screen_width, screen_height),Image.ANTIALIAS))

  upfail_image = ImageTk.PhotoImage(Image.open(str(path + '/images/uploadfail.png'))
    .resize((screen_width/3, screen_height/3),Image.ANTIALIAS))  

  uploaddone_image = ImageTk.PhotoImage(Image.open(str(path + '/images/uploaddone.png'))
    .resize((screen_width/3, screen_height/3),Image.ANTIALIAS))

  
  uploading_image = ImageTk.PhotoImage(Image.open(str(path + '/images/uploading.png'))
    .resize((screen_width/3, screen_height/3),Image.ANTIALIAS))

  load_all_images(250,250)

    
  page = Canvas(tk,width=screen_width, height=screen_height)
  page.pack()
  page.place(x=-1,y=-1)
  
  
  main_page(None)




  


  tk.mainloop()

