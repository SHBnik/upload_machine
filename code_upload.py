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



upload_busy = None
button_images = []


def load_folder_image(size_x,size_y,_path):
  image = ImageTk.PhotoImage(Image.open(_path)
    .resize((size_x, size_y),Image.ANTIALIAS))
  return image

def load_all_images(size_x,size_y):
  global lcd_image,mainboard_image

  lcd_image = ImageTk.PhotoImage(Image.open(str(path + '/images/lcd.png'))
    .resize((size_x, size_y),Image.ANTIALIAS))

  mainboard_image = ImageTk.PhotoImage(Image.open(str(path + '/images/mainboard.png'))
    .resize((size_x, size_y),Image.ANTIALIAS))


  # bride_image = ImageTk.PhotoImage(Image.open(str(path + '/images/bride.png'))
  #   .resize((size_x, size_y),Image.ANTIALIAS))




def on_closing():
  print('bye-bye')
  tk.destroy()




def create_btn(image,pos_x,pos_y,function,_arg):
  btn = page.create_image(pos_x, pos_y, image=image, anchor=NW)
  page.tag_bind(btn, "<Button-1>", lambda event, arg=_arg: function(event, arg))

def clear_page():
  page.delete("all")
  page.create_image(0, 0,anchor=NW, image=background_image)










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


def create_note_box(note):
  note_box = Canvas(tk,width=screen_width/2, height=screen_height/2)
  note_box.pack()
  note_box.place(x=10,y=10)
  note_box.create_text(10,10,anchor=NW,text=note)
  return note_box













def main_page(event,tmp):
  clear_page()
  create_btn(lcd_image,100,100,lcd_page,None)
  create_btn(mainboard_image,400,100,mainboard_page,None)








def lcd_page(event,tmp):
  clear_page()


def mainboard_page(event,tmp):
  global button_images
  clear_page() 
  button_images = []
  subfolders = list(filter(lambda x: os.path.isdir(os.path.join(str(path+'/mainboards'), x)), os.listdir(str(path+'/mainboards'))))   
  print('this folders found',subfolders)
  for count,folder in enumerate(subfolders):
    button_images.append( load_folder_image(250,250,str(path+'/mainboards'+'/'+folder+'/'+folder+'.png')))
    create_btn(button_images[-1],count*4*100,100,device_page,str(path+'/mainboards'+'/'+folder))



def device_page(event,folder_path):
  global button_images
  clear_page() 
  button_images = []
  subfolders = list(filter(lambda x: os.path.isdir(os.path.join(folder_path, x)), os.listdir(folder_path)))    
  print('this folders found',subfolders)
  for count,folder in enumerate(subfolders):
    button_images.append( load_folder_image(250,250,str(folder_path+'/'+folder+'/'+folder+'.png')))
    create_btn(button_images[-1],count*4*100,100,device_version_page,str(folder_path+'/'+folder))


def device_version_page(event,folder_path):
  clear_page()
  with open(str(folder_path+'/note.txt'), 'r') as version_spec:
    notes = version_spec.read()
  
  nt_box = create_note_box(notes)


def upload_button(event,folder_path):
  
  
  upload_arduino_code('bride')








msg_box = None
def message_box_handler():
  global upload_busy,msg_box
  if upload_busy == True:
    msg_box = create_msg_box(uploading_image)
    upload_busy = None
  elif upload_busy == False:
    destroy_msgbox(msg_box,0)
    msg_box = create_msg_box(uploaddone_image)
    destroy_msgbox(msg_box,5)
    upload_busy = None
  elif upload_busy == None:
    pass

  threading.Timer(0.5, message_box_handler).start()



def upload_cmd(port,machine):
  global upload_busy
  
  upload_busy = True

  os.system('/usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -v -v -v -patmega2560 -cwiring -P'
  +str(port)+' -b115200 -D -Uflash:w:'
  +str(hex_address[machine])+':i')
 
  upload_busy = False


def upload_arduino_code(machine):
  try:
    
    port = [tuple(p) for p in list(serial.tools.list_ports.comports())][0][0]
 
    if(port.find('AMA') != -1):
      raise 'no port found'
    
    
    threading.Thread(target=upload_cmd, args=(port,machine,)).start()
    
 
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
  
  message_box_handler()

  main_page(None,None)




  


  tk.mainloop()

