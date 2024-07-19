import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from ultralytics import YOLO

# This application is designed to detect Jordanian coins using a YOLO model and display their total value.
# It also allows users to select a currency to see the equivalent amount in various currencies.
# The application features a live video stream, real-time coin detection, and currency conversion functionality.

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
      
        self.title("Jordanian Coin Detection")
        self.attributes("-fullscreen", True)
        self.configure(bg="#282c34")


        self.model = YOLO(r'C:\Users\user\Downloads\jdcoins.pt')

      
        self.setup_grid()

    def setup_grid(self):
        self.create_widgets()
        
    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Jordanian Coin Detection", 
                                        fg_color="#282c34", text_color="#61dafb", 
                                        font=("Helvetica", 24))
        self.title_label.grid(row=0, column=0, pady=10)

        self.explanation_label = ctk.CTkLabel(self, text="This application detects Jordanian coins and converts the total value to various currencies.", 
                                              fg_color="#282c34", text_color="white", font=("Helvetica", 14))
        self.explanation_label.grid(row=1, column=0, pady=5)

        self.currency_label = ctk.CTkLabel(self, text="Select Currency:", 
                                          fg_color="#282c34", text_color="white", font=("Helvetica", 14))
        self.currency_label.grid(row=2, column=0, pady=5)
        
        self.currency_var = ctk.StringVar(self)
        self.currency_var.set("Select Currency")
        self.currencies = {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "KRW": "South Korean Won",
            "CNY": "Chinese Yuan",
            "FRF": "French Franc",
            "KWD": "Kuwaiti Dinar",
            "SAR": "Saudi Riyal",
            "AED": "United Arab Emirates Dirham",
            "BHD": "Bahraini Dinar",
            "OMR": "Omani Rial"
        }
        self.currency_menu = ctk.CTkOptionMenu(self, variable=self.currency_var, values=list(self.currencies.keys()), 
                                              corner_radius=10, fg_color="#3b3f4c", button_color="#61dafb", 
                                              button_hover_color="#4d5d6e", command=self.update_conversion)
        self.currency_menu.grid(row=3, column=0, pady=5)

        self.imageFrame = ctk.CTkFrame(self, fg_color="#282c34", width=800, height=600, corner_radius=15)
        self.imageFrame.grid(row=4, column=0, padx=10, pady=10)
        self.imageFrame.grid_propagate(False)

        self.stream_label = ctk.CTkLabel(self.imageFrame, fg_color="#282c34")
        self.stream_label.pack(fill="both", expand=True)

        self.start_button = ctk.CTkButton(self, text="Start Detection", 
                                         fg_color="#282c34", border_width=2, 
                                         border_color="#61dafb", text_color="white", 
                                         width=200, height=50, corner_radius=10, 
                                         hover_color="#4d5d6e", command=self.start_stream)
        self.start_button.grid(row=5, column=0, padx=10, pady=10)

        self.exit = ctk.CTkButton(self, text="EXIT", 
                                 fg_color="#282c34", border_width=2, 
                                 border_color="red", text_color="white", 
                                 width=200, height=50, corner_radius=10, 
                                 hover_color="#4d5d6e", command=self.destroy)
        self.exit.grid(row=6, column=0, padx=10, pady=10)

        self.credits_label = ctk.CTkLabel(self, text="Made by Amal Alkraimeen ❤️", 
                                          fg_color="#282c34", text_color="white")
        self.credits_label.grid(row=7, column=0, pady=10)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.converted_label = None

    def start_stream(self):
        self.cap = cv2.VideoCapture(0)
        self.display()
        
    def display(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.model(frame, conf=0.4)
            frame = self.draw_detections(frame, results)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.stream_label.imgtk = imgtk
            self.stream_label.configure(image=imgtk)
        
        self.after(10, self.display)

    def draw_detections(self, frame, results):
        total_amount = 0
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = self.model.names[int(box.cls.item())]
                conf = box.conf.item()
                denomination = int(label)
                total_amount += denomination
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        
        if self.currency_var.get() != "Select Currency":
            converted_amount = self.convert_currency(total_amount, self.currency_var.get())
            self.update_conversion(converted_amount)
        
        return frame

    def convert_currency(self, amount, target_currency):
        conversion_rates = {
            "USD": 1.41,
            "EUR": 1.19,
            "GBP": 1.0,
            "JPY": 153.54,
            "KRW": 1705.13,
            "CNY": 9.15,
            "FRF": 7.8,   
            "KWD": 0.42,
            "SAR": 5.3,
            "AED": 5.18,
            "BHD": 0.53,
            "OMR": 0.53
        }
        rate = conversion_rates.get(target_currency, 1)
        return amount * rate

    def update_conversion(self, amount=None):
        if amount is not None:
            if self.converted_label:
                self.converted_label.destroy()
            
            country_name = self.currencies.get(self.currency_var.get(), "Currency")
            self.converted_label = ctk.CTkLabel(self, text=f"Converted Amount: {amount:.2f} {country_name}", 
                                                fg_color="#282c34", text_color="#61dafb", 
                                                font=("Helvetica", 18))
            self.converted_label.grid(row=8, column=0, pady=10)
        else:
            if self.converted_label:
                self.converted_label.destroy()
            self.converted_label = ctk.CTkLabel(self, text=f"Converted Amount: {self.convert_currency(0, self.currency_var.get()):.2f} {self.currencies.get(self.currency_var.get(), 'Currency')}", 
                                                fg_color="#282c34", text_color="#61dafb", 
                                                font=("Helvetica", 18))
            self.converted_label.grid(row=8, column=0, pady=10)

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
