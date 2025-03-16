import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd

# Function to calculate carbon footprint
def calculate_carbon_footprint(energy, transport, waste):
    return (energy * 0.5) + (transport * 0.2) + (waste * 0.3)

# Function to generate PDF report
def generate_report(name, energy, transport, waste, footprint):
    # Ensure the reports folder exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Generate the chart
    categories = ['Energy', 'Transport', 'Waste']
    values = [energy, transport, waste]
    plt.bar(categories, values)
    plt.title(f'Carbon Footprint Breakdown for {name}')
    plt.ylabel('Value')
    chart_path = f"reports/{name}_chart.png"
    plt.savefig(chart_path, bbox_inches='tight')  # Ensure the chart fits properly
    plt.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)


    pdf.cell(200, 10, txt=f"Carbon Footprint Report for {name}", ln=True, align="C")
    pdf.ln(10)

    # Add textual report
    pdf.cell(200, 10, txt=f"Energy Usage: {energy} kWh", ln=True)
    pdf.cell(200, 10, txt=f"Transportation: {transport} miles", ln=True)
    pdf.cell(200, 10, txt=f"Waste: {waste} kg", ln=True)
    pdf.cell(200, 10, txt=f"Total Carbon Footprint: {footprint:.2f} tons CO2", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Suggestions to Reduce Carbon Footprint:", ln=True)
    pdf.cell(200, 10, txt="- Use renewable energy sources.", ln=True)
    pdf.cell(200, 10, txt="- Opt for public transportation or carpooling.", ln=True)
    pdf.cell(200, 10, txt="- Recycle and reduce waste.", ln=True)
    pdf.ln(10)

    # Add the chart to the PDF
    pdf.image(chart_path, x=10, y=pdf.get_y(), w=180)  # Add the chart below the text
    pdf.ln(85)


    pdf.output(f"reports/{name}_report.pdf")

# save client data to CSV
def save_client_data(name, energy, transport, waste, footprint):
    file_exists = os.path.isfile("reports/client_data.csv")
    with open("reports/client_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Client Name", "Energy Usage (kWh)", "Transportation (miles)", "Waste (kg)", "Carbon Footprint (tons CO2)"])
        writer.writerow([name, energy, transport, waste, footprint])

#  analyze reports
def analyze_reports():
    try:

        df = pd.read_csv("reports/client_data.csv")


        numeric_data = df.drop(columns=["Client Name"])


        summary = numeric_data.describe()


        summary.to_csv("reports/summary.csv")

        # Generate a bar chart for average values
        averages = numeric_data.mean()
        plt.bar(averages.index, averages.values)
        plt.title('Average Carbon Footprint Metrics')
        plt.ylabel('Average Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("reports/summary_chart.png")
        plt.show()

        messagebox.showinfo("Success", "Summary report generated!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No client data found. Please generate reports first.")


def on_submit():
    try:
        name = entry_name.get()
        energy = float(entry_energy.get())
        transport = float(entry_transport.get())
        waste = float(entry_waste.get())

        footprint = calculate_carbon_footprint(energy, transport, waste)
        generate_report(name, energy, transport, waste, footprint)
        save_client_data(name, energy, transport, waste, footprint)  # Save client data

        messagebox.showinfo("Success", f"Report generated for {name}!")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter numeric values.")

# Create the main window
root = tk.Tk()
root.title("Carbon Footprint Tool")

# Create input fields
tk.Label(root, text="Client Name:").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Energy Usage (kWh):").grid(row=1, column=0, padx=10, pady=5)
entry_energy = tk.Entry(root)
entry_energy.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Transportation (miles):").grid(row=2, column=0, padx=10, pady=5)
entry_transport = tk.Entry(root)
entry_transport.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Waste (kg):").grid(row=3, column=0, padx=10, pady=5)
entry_waste = tk.Entry(root)
entry_waste.grid(row=3, column=1, padx=10, pady=5)


tk.Button(root, text="Generate Report", command=on_submit).grid(row=4, column=0, columnspan=2, pady=10)


tk.Button(root, text="Analyze Reports", command=analyze_reports).grid(row=5, column=0, columnspan=2, pady=10)


root.mainloop()