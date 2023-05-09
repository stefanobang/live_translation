import tkinter as tk
from PIL import Image, ImageTk

class CustomTitleBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#444444")
        self.parent = parent
        self.start_pos = None
        
        # Add title text
        title_label = tk.Label(self, text="liveTranslation Overlay", bg="#444444", fg="white")
        title_label.pack(side="left", padx=10)
        
        # Add close button
        close_button = tk.Button(self, text="X", bg="#444444", fg="white", bd=0, command=self.close_window)
        close_button.pack(side="right", padx=10)
        
        # Bind mouse events to the title bar to handle window movement
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)
        
    def start_move(self, event):
        self.start_pos = (event.x, event.y)
        
    def stop_move(self, event):
        self.start_pos = None
        
    def on_move(self, event):
        if self.start_pos:
            x, y = self.start_pos
            dx = event.x - x
            dy = event.y - y
            self.parent.geometry(f"+{self.parent.winfo_x() + dx}+{self.parent.winfo_y() + dy}")
            
    def close_window(self):
        self.parent.destroy()

def reload_image():
    global photo_image
    # Load the new image
    image = Image.open("./overlay/transcribedImage1.png")
    photo_image = ImageTk.PhotoImage(image)
    
    # Update the Text widget's image
    text.config(state="normal")
    text.delete("1.0", "end")
    text.image_create("end", image=photo_image)
    text.config(state="disabled")
    
    # Schedule the next image reload in 5 seconds
    window.after(5000, reload_image)

# Create the window
window = tk.Tk()

# Set the window to be always on top
window.wm_attributes("-topmost", 1)

# Hide the default window bar
window.overrideredirect(True)

# Set the window size and position
window.geometry("700x150")

# Create the custom title bar
title_bar = CustomTitleBar(window)
title_bar.pack(fill="x")

# Create a Text widget to display the image and allow scrolling
text = tk.Text(window, wrap="none", state="disabled")
text.pack(expand=True, fill="both")

# Load the initial image
image = Image.open("./overlay/transcribedImage.png")
photo_image = ImageTk.PhotoImage(image)
text.config(state="normal")
text.image_create("end", image=photo_image)
text.config(state="disabled")

# Allow scrolling by setting the Text widget's yview method to the Scrollbar's set method
scrollbar = tk.Scrollbar(text.master)
scrollbar.pack(side="right", fill="y")
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)

# Schedule the next image reload in 5 seconds
window.after(5000, reload_image)

# Start the Tkinter event loop
window.mainloop()






# import tkinter as tk
# from PIL import Image, ImageTk

# # Create the window
# window = tk.Tk()
# window.geometry("600x150")
# window.title("liveTranslation Overlay")

# # Set the window to be always on top
# window.wm_attributes("-topmost", 1)

# # Load the image with the text overlay
# # image = Image.open("./overlay/textbox.jpg")
# image = Image.open("testOverlay.png")

# # Create a PhotoImage object to display the image
# photo_image = ImageTk.PhotoImage(image)

# # Create a label to display the image
# label = tk.Label(window, image=photo_image)
# label.pack()

# # Set the label to be always on top of the window
# label.lift()


# # Start the Tkinter event loop
# window.mainloop()