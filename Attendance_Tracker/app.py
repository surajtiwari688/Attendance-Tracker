import tkinter as tk
from tkinter import messagebox
from database import insert_attendance, fetch_history


#Function to Calculate Attendance

def calculate_attendance():
    try:
        total_days = int(total_days_entry.get())
        weekends = int(weekends_entry.get())
        leaves = int(leaves_entry.get())
        office_visits = int(office_visits_entry.get())

        working_days = total_days - weekends
        available_days = working_days - leaves
        required_attendance = int(0.8 * available_days)

        attendance_percentage = (office_visits / available_days) * 100 if available_days > 0 else 0

        # store data in database
        insert_attendance(total_days, weekends, leaves, office_visits, attendance_percentage)

        # show result
        result_text = f"Total Working Days: {working_days}\n"
        result_text += f"Available Days After Leave: {available_days}\n"
        result_text += f"Required Attendance (80%): {required_attendance} days\n"
        result_text += f"Your Attendance: {office_visits} days\n"
        result_text += f"Attendance Percentage: {attendance_percentage:.2f}%\n"

        if office_visits >= required_attendance:
            result_text += "✅ You have met the 80% attendance requirement!"
        else:
            result_text += "❌ You have NOT met the 80% attendance requirement."

        messagebox.showinfo("Attendance Report", result_text)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")

# Function to View Attendance History

def view_history():
    records = fetch_history()

    if not records:
        messagebox.showinfo("History", "No attendance records found.")
        return
    
    history_text = "ID | Total | Weekends | Leaves | Office | % | Date\n"
    history_text += "-" * 70 + "\n"
    
    for record in records:
        history_text += f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]} | {record[5]:.2f}% | {record[6]}\n"

    messagebox.showinfo("Attendance History", history_text)



# Creating GUI
root = tk.Tk()
root.title("Attendance Tracker")
root.geometry("400x400")

# Labels and Entry Fields
tk.Label(root, text="Total Days in Month:").pack()
total_days_entry = tk.Entry(root)
total_days_entry.pack()

tk.Label(root, text="Total Weekends:").pack()
weekends_entry = tk.Entry(root)
weekends_entry.pack()

tk.Label(root, text="Leaves Taken:").pack()
leaves_entry = tk.Entry(root)
leaves_entry.pack()

tk.Label(root, text="Office Visits:").pack()
office_visits_entry = tk.Entry(root)
office_visits_entry.pack()

# Buttons
tk.Button(root, text="Calculate Attendance", command=calculate_attendance).pack()
tk.Button(root, text="View Attendance History", command=view_history).pack()

# Run the GUI Loop
root.mainloop()


