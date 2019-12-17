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
  page.create_text(400,250,fill="darkblue",text="Uploading")
  upload_arduino_code('bride')


















def upload_arduino_code(machine):
  try:
    port = [tuple(p) for p in list(serial.tools.list_ports.comports())][0][0]
    os.system('/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P'
      +str(port)+' -b115200 -D -Uflash:w:'
      +str(hex_address[machine])+':i')
  except Exception as e:
    print('error in upload arduino',e)

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

  load_all_images(250,250)

    
  page = Canvas(tk,width=screen_width, height=screen_height)
  page.pack()
  page.place(x=-1,y=-1)
  
  
  main_page(None)




  


  tk.mainloop()

