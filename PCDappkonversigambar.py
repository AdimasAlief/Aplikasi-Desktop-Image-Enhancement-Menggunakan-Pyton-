#beberapa library yang di gunakan 
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Variabel global untuk menyimpan gambar yang diimpor dan diproses
img = None
img_tk = None
img_cv = None
output_img = None 

#Fungsi untuk import gambar dari file 
def import_image():
    global img, img_tk, img_cv, output_img
    sharpness_slider.config(state=tk.DISABLED)
    brightness_slider.config(state=tk.DISABLED)
    color_slider.config(state=tk.DISABLED)

    file_path = filedialog.askopenfilename(

# gambar yang bisa di input berupa jpg,jpeg,png,gif
        filetypes=[("Image Files", ".jpg;.jpeg;.png;.bmp;.gif")])
    if file_path:
        img = Image.open(file_path)
        img = img.resize((300, 300), Image.LANCZOS)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        img_tk = ImageTk.PhotoImage(img)
        label_input.config(image=img_tk)
        label_input.image = img_tk

        label_output.config(image='')
        label_output.image = None
        output_img = None  

    sharpness_slider.config(state=tk.NORMAL)
    brightness_slider.config(state=tk.NORMAL)
    color_slider.config(state=tk.NORMAL)

#Fungsi untuk mengubah gambar ke grayscale dan menampilkanya di kolom kedua atau kolom output
def convert_to_grayscale():
    global img, img_tk, img_cv, output_img
    if img:
        gray_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        output_img = Image.fromarray(gray_cv)
        gray_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(gray_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk mengubah gambar ke bianry (hitam putih) dan menampilkanya di kolom kedua atau kolom output
def convert_to_binary():
    global img, img_cv, img_tk, output_img
    if img:
        gray_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        binary_cv = cv2.adaptiveThreshold(gray_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
        output_img = Image.fromarray(binary_cv)
        binary_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(binary_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk mengubah gambar ke negative dan menampilkanya di kolom kedua atau kolom output
def convert_to_negative():
    global img, img_tk, img_cv, output_img
    if img:
        negative_cv = cv2.bitwise_not(img_cv)
        output_img = Image.fromarray(negative_cv)
        negative_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(negative_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk meningkatkan ketajaman gambar seuai keinginan user melalui tombol slider dan menampilkanya di kolom kedua atau kolom output       
def enhance_sharpness(value):
    global img, img_cv, img_tk, output_img
    if img:
        sharpen_value = float(value)
        kernel = np.array([[-1, -1, -1],
                           [-1, 9 + sharpen_value, -1],
                           [-1, -1, -1]])
        sharpened_cv = cv2.filter2D(img_cv, -1, kernel)
        output_img = Image.fromarray(sharpened_cv)
        sharpened_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(sharpened_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk meningkatkan pengcahayaan gambar sesuai keinginan user melalui tombol slider dan menampilkanya di kolom kedua atau kolom output 
def adjust_brightness(value):
    global img, img_cv, img_tk, output_img
    if img:
        brightness = int(value)
        adjusted_cv = cv2.convertScaleAbs(img_cv, alpha=1, beta=brightness)
        output_img = Image.fromarray(adjusted_cv)
        brightness_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(brightness_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk meningkatkan warna gambar sesuai keinginan user melalui tombol slider dan menampilkanya di kolom kedua atau kolom output 
def adjust_color_intensity(value):
    global img, img_cv, img_tk, output_img
    if img:
        color_intensity = float(value)
        hsv_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        hsv_img[:, :, 1] = cv2.multiply(hsv_img[:, :, 1], color_intensity)
        adjusted_cv = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        output_img = Image.fromarray(adjusted_cv)
        color_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(color_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk

#Fungsi untuk mengurangi noise pada gambar dan menampilkanya di kolom kedua atau kolom output
def reduce_noise():
    global img, img_cv, img_tk, output_img
    if img:
        noise_reduced_cv = cv2.bilateralFilter(img_cv, d=9, sigmaColor=75, sigmaSpace=75)
        output_img = Image.fromarray(noise_reduced_cv)
        noise_reduced_img = output_img.resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(noise_reduced_img)
        label_output.config(image=img_tk)
        label_output.image = img_tk
        
#Fungsi untuk menyimpan gambar dari hasil perubahan gambar ke file 
def save_image():
    global output_img
    if output_img:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", ".*")]
        )
        if file_path:
            output_img.save(file_path)

# Inisialisasi jendela utama aplikasi
root = tk.Tk()
root.title("Citra Digital")

# di gunakan untuk menentukan ukuran dan posisi layar desktop yang muncul 
window_width = 990
window_height = 680  

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
root.configure(bg='#2e2e2e')

#Frame yang di gunakan untuk menampilkan gambar import
frame_input = tk.Frame(root, bg='#2e2e2e', width=350, height=window_height)
frame_input.grid(row=0, column=0, padx=5, pady=5)
frame_input.pack_propagate(False)

label_input = tk.Label(frame_input, bg="#1e1e1e")
label_input.pack(expand=True)

# Frame yang di gunakan untuk menampilkan gambar output
frame_output = tk.Frame(root, bg='#2e2e2e', width=350, height=window_height)
frame_output.grid(row=0, column=2, padx=5, pady=0)
frame_output.pack_propagate(False)

label_output = tk.Label(frame_output, bg="#1e1e1e")
label_output.pack(expand=True)

## Frame yang di gunakan untuk menempatkan kontrol (tombol dan slider)
frame_controls = tk.Frame(root, bg='#2e2e2e')
frame_controls.grid(row=0, column=1, padx=5, pady=0)

## Tombol yang di gunakan untuk mengimpor gambar
button_import = tk.Button(frame_controls, text="Import Gambar", command=import_image,
                          font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_import.grid(row=0, column=0, padx=5, pady=5)

# Tombol yang di gunakan untuk mengonversi gambar menjadi grayscale
button_grayscale = tk.Button(frame_controls, text="Konversi Grayscale", command=convert_to_grayscale,
                             font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_grayscale.grid(row=1, column=0, padx=5, pady=5)

# Tombol yang di gunakan untuk mengonversi gambar menjadi biner
button_binary = tk.Button(frame_controls, text="Konversi Biner", command=convert_to_binary,
                          font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_binary.grid(row=2, column=0, padx=5, pady=5)

# Tombol yang di gunakan untuk mengonversi gambar menjadi negatif
button_negative = tk.Button(frame_controls, text="Konversi Negatif", command=convert_to_negative,
                            font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_negative.grid(row=3, column=0, padx=5, pady=5)

# Slider yang di gunakan untuk menyesuaikan ketajaman gambar
sharpness_slider = tk.Scale(frame_controls, from_=0.0, to=10.0, resolution=0.1, orient="horizontal",
                            label="Tingkatkan Ketajaman", length=250, command=enhance_sharpness,
                            font=('Helvetica', 10), bg='#4e4e4e', fg='white', troughcolor='#3e3e3e',
                            activebackground='#6e6e6e', highlightthickness=0)
sharpness_slider.grid(row=5, column=0, padx=5, pady=5)

## Slider yang di gunakan untuk menyesuaikan atau mengatur kecerahan gambar
brightness_slider = tk.Scale(frame_controls, from_=0, to=255, orient="horizontal",
                             label="Sesuaikan Kecerahan", length=250, command=adjust_brightness,
                             font=('Helvetica', 10), bg='#4e4e4e', fg='white', troughcolor='#3e3e3e',
                             activebackground='#6e6e6e', highlightthickness=0)
brightness_slider.grid(row=6, column=0, padx=5, pady=5)

# Slider yang di gunakan untuk menyesuaikan intensitas warna gambar atau mengatur warna gambar 
color_slider = tk.Scale(frame_controls, from_=0.0, to=2.0, resolution=0.1, orient="horizontal",
                        label="Intensitas Warna", length=250, command=adjust_color_intensity,
                        font=('Helvetica', 10), bg='#4e4e4e', fg='white', troughcolor='#3e3e3e',
                        activebackground='#6e6e6e', highlightthickness=0)
color_slider.grid(row=7, column=0, padx=5, pady=5)

# Tombol yang di gunakan untuk mengurangi noise pada gambar
button_reduce_noise = tk.Button(frame_controls, text="Kurangi Noise", command=reduce_noise,
                                font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_reduce_noise.grid(row=8, column=0, padx=5, pady=5)

# Tombol yang di gunakan untuk menyimpan gambar hasil pemrosesan ke file 
button_save = tk.Button(frame_controls, text="Simpan Gambar", command=save_image,
                        font=('Helvetica', 12), bg='#4e4e4e', fg='white', width=20)
button_save.grid(row=9, column=0, padx=5, pady=5)

# di gunakan untuk menjalankan loop utama aplikasi
root.mainloop()
