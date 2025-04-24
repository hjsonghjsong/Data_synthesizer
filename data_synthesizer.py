import tkinter as tk
import random
import json
from datetime import datetime
import os
import pyautogui
from tkcalendar import DateEntry  # For date picker widget

class App:


    def generate_json_filepath(self):
        json_file_path = os.path.join('logs', 'sanitized_json', f"{self.json_current_filename}.json")
        return json_file_path

    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Position Tracker")
        
        # Set window size
        self.root.geometry("1920x1080+0+0")
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create main container frame
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas frame
        self.canvas_frame = tk.Frame(self.main_container)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create white canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=1720, height=1080, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create control frame on the right
        self.control_frame = tk.Frame(self.main_container, bg='lightgray', width=200)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Initialize list to store labels
        self.labels = []
        
        # Add auto-generate button
        self.auto_generate_button = tk.Button(
            self.control_frame,
            text="Start Auto Generate",
            command=self.toggle_auto_generate,
            bg='lightblue',
            padx=20,
            pady=10,
            font=('Arial', 10, 'bold')
        )
        self.auto_generate_button.pack(side=tk.TOP, padx=20, pady=20)
        
        # Initialize auto-generate state
        self.auto_generating = False
        self.auto_generate_job = None
        
        # Create logs directory and subdirectories
        os.makedirs('logs/sanitized_json', exist_ok=True)
        os.makedirs('logs/screenshots', exist_ok=True)
        
        # Initialize file index
        self.file_index = 0
        # Initialize event counter
        self.event_counter = 0
        # Generate initial filename
        self.json_current_filename_header = "sanitized_" + datetime.now().strftime("%Y%m%d_%H%M%S") + "_" 
        self.json_current_filename = self.json_current_filename_header + f"{self.file_index:04d}"
        self.json_file_path = self.generate_json_filepath()
        
        header = self.generate_file_header()
        with open(self.json_file_path, 'w') as f:    
            f.write(header)
        

        self.event_threshold = 5   # how many clicks before generating a new file

        # Bind mouse click to canvas
        self.canvas.bind("<Button-1>", self.on_click)
    
    def get_global_screen_coordinates(self, event):
        x = event.x
        y = event.y

        # Convert canvas coordinates to screen coordinates
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        canvas_x = self.canvas.winfo_x()
        canvas_y = self.canvas.winfo_y()
        # Add offsets to get global screen coordinates
        global_screen_x = x + root_x + canvas_x
        global_screen_y = y + root_y + canvas_y

        # Print canvas and root coordinates
        #print(f"Root coordinates: ({root_x}, {root_y})")
        #print(f"Canvas coordinates: ({canvas_x}, {canvas_y})")
        


        return global_screen_x, global_screen_y
    

    
    def on_click(self, event):
        
        
        
        if self.event_counter > self.event_threshold:
            tail=self.generate_file_tail()
            with open(self.json_file_path, 'a+') as f:    
                f.write(tail)

            self.event_counter = 0  # Reset counter
            
            
            self.file_index += 1
            self.json_current_filename = self.json_current_filename_header + f"{self.file_index:04d}"
            self.json_file_path = self.generate_json_filepath()
            
            header = self.generate_file_header()
            with open(self.json_file_path, 'w') as f:    
                f.write(header)


   
        global_screen_x, global_screen_y = self.get_global_screen_coordinates(event)
        # Increment event counter
        self.event_counter += 1
        
        # Create event data
        click_data = {
            "event": "MOUSE",
            "event_type": "SINGLE_CLICK",
            "button": "Button.left",
            "x": global_screen_x,
            "y": global_screen_y,
            "timestamp": datetime.now().isoformat()
        }

        # Draw random shape
        #self.draw_shape(event)
        self.draw_UI_elements(event)
        
        self.root.update_idletasks()
        self.root.update()


        if self.event_counter > 1:
            with open(self.json_file_path, 'a+') as f:
                f.write(",\n")
        # Write JSON formatted data to file
        with open(self.json_file_path, 'a+') as f:
            json.dump(click_data, f, indent=4)
        
            
        screenshot_filename = f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        screenshot_path = os.path.join("logs/screenshots", screenshot_filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)






    def generate_file_header(self): 
        metadata = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "type": "sanitized_keystroke_data", 
                "version": "1.0",
                "contains_sensitive_data": False,
                "sanitization_applied": True
            }
        }
        
        # Convert to JSON string with indentation and newlines
        data = json.dumps(metadata, indent=4)
        
     
   
        # Add newlines after commas
        data = data.replace(",", ",\n")
        # Truncate last 2 characters from data
        data = data[:-2]
        data = data + ",  \n  \"events\" : ["
        #print("Generated header:")
        #print(data)
        #print("===")
        return data




    def generate_file_tail(self):

        data = "],\n  \"text_summary\": {\n    \"original_length\": 0,\n    \"sanitized_length\": 0,\n    \"password_locations_count\": 0\n  }\n}"

        #print("Generated tail:")
        #print(data)
        #print("===")
        
        return data
       
        
        # Convert to JSON string with indentation and newlines
        json_str = json.dumps(metadata, indent=4)
        
        # Add newlines after commas
        data = json_str.replace(",", ",\n") + "\n"
        return data

    def get_random_ui_color(self):
        # Generate random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_UI_elements(self, event):
        x = event.x
        y = event.y
        
        # Generate random properties
        width = random.randint(80, 200)
        height = random.randint(25, 40)
        


        
        # Calculate position (centered on click)
        x1 = x - width/2
        y1 = y - height/2
        x2 = x + width/2
        y2 = y + height/2
        
        # Clear previous elements
        self.canvas.delete("all")
        # Clear previous labels
        for label in self.labels:
            label.destroy()
        self.labels = []
        
        # Randomly choose UI element type
        ui_type = random.choice(["button", "label", "datepicker", "checkbox"])
        

        
        # Get color for this UI element
        color = self.get_random_ui_color()


        
        if ui_type == "button":
            # Draw button rectangle
                        # Add button text
            button_text = random.choice(["Submit", "Cancel", "OK", "Save"])
            # Create button widget
            button = tk.Button(
                self.canvas,
                text=button_text,
                bg=color,
                relief="raised",
                font=('Arial', 10),
                padx=10,
                pady=5
            )
            # Place button at click coordinates
            button.place(x=x1, y=y1, width=width, height=height)
            self.labels.append(button)  # Store reference to remove later
          

            
            
        elif ui_type == "label":
            # Generate random label text
            label_options = [
                "First Name:", "Last Name:", "Phone Number:", "Address:", 
                "Company:", "Department:", "Employee ID:", "Start Date:",
                "Account Number:", "Order ID:", "Customer ID:", "Status:",
                "Description:", "Category:", "Priority:", "Due Date:"
            ]
            label_text = random.choice(label_options)
            
            # Create and place label with black text and random background
            label = tk.Label(
                self.canvas,
                text=label_text,
                font=('Arial', 12),
                fg='black',
                bg=color
            )
            label.place(x=x, y=y)
            self.labels.append(label)  # Store reference to label
            
        elif ui_type == "datepicker":
            # Generate random date between 2020-2025
            random_date = datetime(
                random.randint(2020, 2025),
                random.randint(1, 12), 
                random.randint(1, 28)
            )
            
            # Create date picker widget with black text and random background
            date_picker = DateEntry(
                self.canvas,
                width=12,
                background=color,
                foreground='black',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                firstweekday='sunday'
            )
            date_picker.set_date(random_date)
            date_picker.place(x=x1, y=y1)
            self.labels.append(date_picker)  # Store reference to remove later
            
        else: # checkbox
            # Generate random checkbox text
            checkbox_options = [
                "Enable notifications", "Remember me", "I agree to terms",
                "Subscribe to newsletter", "Auto-save changes", "Dark mode",
                "Show preview", "Allow cookies", "Sync data", "Stay signed in",
                "Send usage statistics", "Enable auto-update"
            ]
            checkbox_text = random.choice(checkbox_options)
            
            # Create checkbox widget with black text and random background
            checkbox = tk.Checkbutton(
                self.canvas,
                text=checkbox_text,
                bg=color,
                fg='black',
                font=('Arial', 10)
            )
            # Set random enabled status
            checkbox.select() if random.choice([True, False]) else checkbox.deselect()
            checkbox.place(x=x1, y=y1)
            self.labels.append(checkbox)  # Store reference to remove later
            
        # Add coordinates text
        global_screen_x, global_screen_y = self.get_global_screen_coordinates(event)
        coord_text = f"({int(global_screen_x)}, {int(global_screen_y)})"
        self.canvas.create_text(x2+100, y2+1, text=coord_text, 
                              anchor="se", fill="black")




    def draw_shape(self, event):

        x=event.x
        y=event.y


        
        # Generate random properties
        size = random.randint(50, 150)
        # Generate random RGB values
        r = random.randint(0, 255)
        g = random.randint(0, 255) 
        b = random.randint(0, 255)
        # Convert to hex color string
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        
        shape_type = random.randint(0, 2)  # 0=circle, 1=rectangle, 2=oval
       

        
        # Calculate shape coordinates (centered on click)
        x1 = x - size/2  # Top left x
        y1 = y - size/2  # Top left y
        x2 = x + size/2  # Bottom right x 
        y2 = y + size/2  # Bottom right y
     
        # Clear previous shapes
        self.canvas.delete("all")


        # Get random shape type
        shapes = ["circle", "rectangle", "oval"]
        shape = random.choice(shapes)
        
        # Draw the random shape
        if shape == "circle":
            self.canvas.create_oval(x1, y1, x2, y2, fill=color)
        elif shape == "rectangle": 
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        else:
            # Oval is wider than tall
            self.canvas.create_oval(x1-25, y1, x2+25, y2, fill=color)
      

        global_screen_x, global_screen_y = self.get_global_screen_coordinates(event)
        # Add text showing coordinates
        coord_text = f"({int(global_screen_x)}, {int(global_screen_y)})"
        self.canvas.create_text(x2+100, y2+1, text=coord_text, anchor="se", fill="black")

    def on_closing(self):

        print("Bye! Thanks for using the application.")
        tail=self.generate_file_tail()
        with open(self.json_file_path, 'a+') as f:    
                f.write(tail)
        f.close()

        self.root.destroy()  # Close the window

    def toggle_auto_generate(self):
        if not self.auto_generating:
            self.auto_generating = True
            self.auto_generate_button.config(font=('Arial', 10, 'bold'))
            self.auto_generate_button.config(text="Stop Auto Generate", bg='red')
            # Generate one random click immediately
            self.generate_random_click()
        else:
            self.auto_generating = False
            self.auto_generate_button.config(font=('Arial', 10, 'bold'))
            self.auto_generate_button.config(text="Start Auto Generate", bg='lightblue')

    def generate_random_click(self):
        # Generate random coordinates
        x = random.randint(0, self.canvas.winfo_width())
        y = random.randint(0, self.canvas.winfo_height())
        
        # Create fake event
        class FakeEvent:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        fake_event = FakeEvent(x, y)
        
        # Call on_click with fake event
        self.on_click(fake_event)
        
        # If auto-generating is still on, schedule next click
        if self.auto_generating:
            self.auto_generate_job = self.root.after(1000, self.generate_random_click)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
