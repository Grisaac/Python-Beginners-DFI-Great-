import sqlite3

def setup_database():
    conn = sqlite3.connect('hotel_reservation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_name TEXT,
        room_number INTEGER,
        room_type TEXT,
        check_in_date TEXT,
        check_out_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        room_number INTEGER PRIMARY KEY,
        room_type TEXT,
        status TEXT
    )
    ''')
    
    room_types = ['Single', 'Double', 'Suite', 'Deluxe', 'Penthouse']
    room_data = [(101, 'Single', 'Available'),
                 (102, 'Double', 'Available'),
                 (103, 'Suite', 'Available'),
                 (201, 'Deluxe', 'Available'),
                 (202, 'Penthouse', 'Available')]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO rooms (room_number, room_type, status)
    VALUES (?, ?, ?)
    ''', room_data)
    
    conn.commit()
    conn.close()

setup_database()

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Great's Hotel Reservation System")
        self.root.geometry("700x500")
        self.root.configure(bg='#f5f5f5')  

        self.frames = {}
        self.setup_frames()

    def setup_frames(self):
        for F in (HomePage, ReservationPage, ViewReservationsPage, CancelReservationPage, AdminPage,
                  RoomAvailabilityPage, AboutPage, RoomDetailsPage, UpdateReservationPage, ReservationHistoryPage,
                  FeedbackPage):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f8ff')
        self.controller = controller

        tk.Label(self, text="Home Page", font=("Helvetica", 24, "bold"), bg='#f0f8ff').pack(pady=20)

        buttons = [
            ("Make Reservation", "ReservationPage"),
            ("View Reservations", "ViewReservationsPage"),
            ("Cancel Reservation", "CancelReservationPage"),
            ("Admin", "AdminPage"),
            ("Room Availability", "RoomAvailabilityPage"),
            ("About", "AboutPage"),
            ("Room Details", "RoomDetailsPage"),
            ("Update Reservation", "UpdateReservationPage"),
            ("Reservation History", "ReservationHistoryPage"),
            ("Feedback", "FeedbackPage")
        ]
        for text, page in buttons:
            tk.Button(self, text=text, command=lambda p=page: controller.show_frame(p),
                      bg='#4682b4', fg='white', font=("Helvetica", 12, "bold"), padx=10, pady=5).pack(pady=5)

class ReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#e0ffff')
        self.controller = controller

        tk.Label(self, text="Make a Reservation", font=("Helvetica", 24, "bold"), bg='#e0ffff').pack(pady=20)

        tk.Label(self, text="Guest Name:", bg='#e0ffff').pack(pady=5)
        self.guest_name = tk.Entry(self, width=40)
        self.guest_name.pack(pady=5)

        tk.Label(self, text="Room Type:", bg='#e0ffff').pack(pady=5)
        self.room_type = tk.StringVar()
        self.room_type_dropdown = ttk.Combobox(self, textvariable=self.room_type, values=self.get_room_types())
        self.room_type_dropdown.pack(pady=5)

        tk.Label(self, text="Room Number:", bg='#e0ffff').pack(pady=5)
        self.room_number = tk.StringVar()
        self.room_number_dropdown = ttk.Combobox(self, textvariable=self.room_number)
        self.room_number_dropdown.pack(pady=5)

        tk.Label(self, text="Check-In Date (YYYY-MM-DD):", bg='#e0ffff').pack(pady=5)
        self.check_in_date = tk.Entry(self, width=40)
        self.check_in_date.pack(pady=5)

        tk.Label(self, text="Check-Out Date (YYYY-MM-DD):", bg='#e0ffff').pack(pady=5)
        self.check_out_date = tk.Entry(self, width=40)
        self.check_out_date.pack(pady=5)

        tk.Button(self, text="Submit Reservation", command=self.submit_reservation, bg='#32cd32', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

        self.room_type.trace_add("write", self.update_room_numbers)

    def get_room_types(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT room_type FROM rooms')
        room_types = [row[0] for row in cursor.fetchall()]
        conn.close()
        return room_types

    def update_room_numbers(self, *args):
        room_type = self.room_type.get()
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT room_number FROM rooms WHERE room_type = ? AND status = ?', (room_type, 'Available'))
        room_numbers = [row[0] for row in cursor.fetchall()]
        self.room_number_dropdown['values'] = room_numbers
        conn.close()

    def submit_reservation(self):
        guest_name = self.guest_name.get()
        room_number = self.room_number.get()
        room_type = self.room_type.get()
        check_in_date = self.check_in_date.get()
        check_out_date = self.check_out_date.get()

        if not guest_name or not room_number or not check_in_date or not check_out_date:
            messagebox.showerror("Error", "All fields must be filled")
            return

        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO reservations (guest_name, room_number, room_type, check_in_date, check_out_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (guest_name, room_number, room_type, check_in_date, check_out_date))

        cursor.execute('''
        UPDATE rooms
        SET status = ?
        WHERE room_number = ?
        ''', ('Occupied', room_number))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Reservation made successfully")
        self.controller.show_frame("HomePage")

class ViewReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f5f5dc')
        self.controller = controller

        tk.Label(self, text="View Reservations", font=("Helvetica", 24, "bold"), bg='#f5f5dc').pack(pady=20)

        self.reservations_list = tk.Text(self, height=15, width=85, bg='#f0f8ff', fg='#00008b', font=("Helvetica", 12))
        self.reservations_list.pack(pady=10)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)
        
        self.update_reservations()

    def update_reservations(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM reservations')
        reservations = cursor.fetchall()

        self.reservations_list.delete(1.0, tk.END)
        for res in reservations:
            self.reservations_list.insert(tk.END, f"ID: {res[0]}, Guest: {res[1]}, Room: {res[2]}, Type: {res[3]}, Check-In: {res[4]}, Check-Out: {res[5]} \n")
        conn.close()

class CancelReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#ffe4e1')
        self.controller = controller

        tk.Label(self, text="Cancel Reservation", font=("Helvetica", 24, "bold"), bg='#ffe4e1').pack(pady=20)

        tk.Label(self, text="Reservation ID:", bg='#ffe4e1').pack(pady=5)
        self.reservation_id = tk.Entry(self, width=40)
        self.reservation_id.pack(pady=5)

        tk.Button(self, text="Cancel Reservation", command=self.cancel_reservation, bg='#ff6347', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

    def cancel_reservation(self):
        reservation_id = self.reservation_id.get()

        if not reservation_id:
            messagebox.showerror("Error", "Reservation ID must be provided")
            return

        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT room_number FROM reservations WHERE id = ?', (reservation_id,))
        result = cursor.fetchone()

        if result:
            room_number = result[0]
            cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
            cursor.execute('UPDATE rooms SET status = ? WHERE room_number = ?', ('Available', room_number))
            conn.commit()
            messagebox.showinfo("Success", "Reservation cancelled successfully")
        else:
            messagebox.showerror("Error", "Reservation ID not found")

        conn.close()
        self.controller.show_frame("HomePage")

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0e68c')
        self.controller = controller

        tk.Label(self, text="Admin Page", font=("Helvetica", 24, "bold"), bg='#f0e68c').pack(pady=20)

        self.update_rooms()

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

    def update_rooms(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms')
        rooms = cursor.fetchall()

        room_list = tk.Text(self, height=15, width=85, bg='#e6e6fa', fg='#00008b', font=("Helvetica", 12))
        room_list.pack(pady=10)
        room_list.delete(1.0, tk.END)
        for room in rooms:
            room_list.insert(tk.END, f"Room Number: {room[0]}, Type: {room[1]}, Status: {room[2]}\n")

        conn.close()

class RoomAvailabilityPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#e0ffff')
        self.controller = controller

        tk.Label(self, text="Room Availability", font=("Helvetica", 24, "bold"), bg='#e0ffff').pack(pady=20)

        self.room_type = tk.StringVar()
        tk.Label(self, text="Select Room Type:", bg='#e0ffff').pack(pady=5)
        self.room_type_dropdown = ttk.Combobox(self, textvariable=self.room_type, values=self.get_room_types())
        self.room_type_dropdown.pack(pady=5)

        tk.Button(self, text="Check Availability", command=self.check_availability, bg='#32cd32', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

        self.availability_list = tk.Text(self, height=15, width=85, bg='#e6e6fa', fg='#00008b', font=("Helvetica", 12))
        self.availability_list.pack(pady=10)

    def get_room_types(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT room_type FROM rooms')
        room_types = [row[0] for row in cursor.fetchall()]
        conn.close()
        return room_types

    def check_availability(self):
        room_type = self.room_type.get()

        if not room_type:
            messagebox.showerror("Error", "Please select a room type")
            return

        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE room_type = ? AND status = ?', (room_type, 'Available'))
        rooms = cursor.fetchall()

        self.availability_list.delete(1.0, tk.END)
        if rooms:
            for room in rooms:
                self.availability_list.insert(tk.END, f"Room Number: {room[0]}, Type: {room[1]}, Status: {room[2]}\n")
        else:
            self.availability_list.insert(tk.END, "No available rooms for this type")

        conn.close()

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f5deb3')
        self.controller = controller

        tk.Label(self, text="About This App", font=("Helvetica", 24, "bold"), bg='#f5deb3').pack(pady=20)

        tk.Label(self, text="Welcome to the Great's Hotel Reservation System.\n\n"
                             "This application allows you to make, view, and manage hotel reservations.\n"
                             "Features include room availability checking, reservation cancellation, and more.\n\n"
                             "Developed by: Okeleke Great", bg='#f5deb3', font=("Helvetica", 14)).pack(pady=20)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

class RoomDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#d3ffd3')
        self.controller = controller

        tk.Label(self, text="Room Details", font=("Helvetica", 24, "bold"), bg='#d3ffd3').pack(pady=20)

        self.room_number = tk.StringVar()
        tk.Label(self, text="Select Room Number:", bg='#d3ffd3').pack(pady=5)
        self.room_number_dropdown = ttk.Combobox(self, textvariable=self.room_number, values=self.get_room_numbers())
        self.room_number_dropdown.pack(pady=5)

        tk.Button(self, text="Get Details", command=self.show_room_details, bg='#32cd32', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

        self.details_text = tk.Text(self, height=15, width=70, bg='#e6e6fa', fg='#00008b', font=("Helvetica", 12))
        self.details_text.pack(pady=10)

    def get_room_numbers(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT room_number FROM rooms')
        room_numbers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return room_numbers

    def show_room_details(self):
        room_number = self.room_number.get()
        if not room_number:
            messagebox.showerror("Error", "Please select a room number")
            return

        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rooms WHERE room_number = ?', (room_number,))
        room = cursor.fetchone()

        if room:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Room Number: {room[0]}\nType: {room[1]}\nStatus: {room[2]}")
        else:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "Room not found")

        conn.close()

class UpdateReservationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#fafad2')
        self.controller = controller

        tk.Label(self, text="Update Reservation", font=("Helvetica", 24, "bold"), bg='#fafad2').pack(pady=20)

        tk.Label(self, text="Reservation ID:", bg='#fafad2').pack(pady=5)
        self.reservation_id = tk.Entry(self, width=40)
        self.reservation_id.pack(pady=5)

        tk.Label(self, text="New Room Number:", bg='#fafad2').pack(pady=5)
        self.new_room_number = tk.StringVar()
        self.new_room_number_dropdown = ttk.Combobox(self, textvariable=self.new_room_number, values=self.get_room_numbers())
        self.new_room_number_dropdown.pack(pady=5)

        tk.Label(self, text="New Check-In Date (YYYY-MM-DD):", bg='#fafad2').pack(pady=5)
        self.new_check_in_date = tk.Entry(self, width=40)
        self.new_check_in_date.pack(pady=5)

        tk.Label(self, text="New Check-Out Date (YYYY-MM-DD):", bg='#fafad2').pack(pady=5)
        self.new_check_out_date = tk.Entry(self, width=40)
        self.new_check_out_date.pack(pady=5)

        tk.Button(self, text="Update Reservation", command=self.update_reservation, bg='#32cd32', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

    def get_room_numbers(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT room_number FROM rooms WHERE status = ?', ('Available',))
        room_numbers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return room_numbers

    def update_reservation(self):
        reservation_id = self.reservation_id.get()
        new_room_number = self.new_room_number.get()
        new_check_in_date = self.new_check_in_date.get()
        new_check_out_date = self.new_check_out_date.get()

        if not reservation_id or not new_room_number or not new_check_in_date or not new_check_out_date:
            messagebox.showerror("Error", "All fields must be filled")
            return

        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()

        cursor.execute('SELECT room_number FROM reservations WHERE id = ?', (reservation_id,))
        old_room_number = cursor.fetchone()

        if old_room_number:
            old_room_number = old_room_number[0]
            cursor.execute('''
            UPDATE reservations
            SET room_number = ?, check_in_date = ?, check_out_date = ?
            WHERE id = ?
            ''', (new_room_number, new_check_in_date, new_check_out_date, reservation_id))

            cursor.execute('UPDATE rooms SET status = ? WHERE room_number = ?', ('Available', old_room_number))
            cursor.execute('UPDATE rooms SET status = ? WHERE room_number = ?', ('Occupied', new_room_number))

            conn.commit()
            messagebox.showinfo("Success", "Reservation updated successfully")
        else:
            messagebox.showerror("Error", "Reservation ID not found")

        conn.close()
        self.controller.show_frame("HomePage")

class ReservationHistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#e6e6fa')
        self.controller = controller

        tk.Label(self, text="Reservation History", font=("Helvetica", 24, "bold"), bg='#e6e6fa').pack(pady=20)

        self.history_list = tk.Text(self, height=15, width=85, bg='#f0f8ff', fg='#00008b', font=("Helvetica", 12))
        self.history_list.pack(pady=10)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)
        
        self.update_history()

    def update_history(self):
        conn = sqlite3.connect('hotel_reservation.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM reservations ORDER BY check_in_date DESC')
        reservations = cursor.fetchall()

        self.history_list.delete(1.0, tk.END)
        for res in reservations:
            self.history_list.insert(tk.END, f"ID: {res[0]}, Guest: {res[1]}, Room: {res[2]}, Type: {res[3]}, Check-In: {res[4]}, Check-Out: {res[5]}\n")

        conn.close()

class FeedbackPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0fff0')
        self.controller = controller

        tk.Label(self, text="Feedback", font=("Helvetica", 24, "bold"), bg='#f0fff0').pack(pady=20)

        tk.Label(self, text="Your Feedback:", bg='#f0fff0').pack(pady=5)
        self.feedback_text = tk.Text(self, height=10, width=60, bg='#e6e6fa', fg='#00008b', font=("Helvetica", 12))
        self.feedback_text.pack(pady=10)

        tk.Button(self, text="Submit Feedback", command=self.submit_feedback, bg='#32cd32', fg='white', font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), bg='#ff4500', fg='white', font=("Helvetica", 12, "bold")).pack(pady=5)

    def submit_feedback(self):
        feedback = self.feedback_text.get("1.0", tk.END).strip()

        if not feedback:
            messagebox.showerror("Error", "Feedback cannot be empty")
            return

        messagebox.showinfo("Thank You", "Feedback submitted successfully")
        self.feedback_text.delete("1.0", tk.END)
        self.controller.show_frame("HomePage")

if __name__ == "__main__":
    root = tk.Tk()
    setup_database() 
    app = HotelApp(root)
    root.mainloop()
