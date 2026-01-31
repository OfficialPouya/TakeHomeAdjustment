import tkinter as tk
from tkinter import ttk, messagebox

class TrueHourlyWageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("True Hourly Wage Calculator")
        self.root.geometry("800x600")
        
        # Basic variables
        self.paycheck_var = tk.DoubleVar(value=2000)
        self.daily_hours_var = tk.DoubleVar(value=8)
        self.work_days_var = tk.DoubleVar(value=5)
        self.commute_minutes_var = tk.DoubleVar(value=30)
        self.daily_costs_var = tk.DoubleVar(value=5)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Basic input fields
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="True Hourly Wage Calculator", 
                 font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Pay information
        pay_frame = ttk.LabelFrame(main_frame, text="Pay Information", padding=10)
        pay_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(pay_frame, text="Take-home Pay:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(pay_frame, textvariable=self.paycheck_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(pay_frame, text="$").grid(row=0, column=2, sticky='w')
        
        # Work schedule
        work_frame = ttk.LabelFrame(main_frame, text="Work Schedule", padding=10)
        work_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(work_frame, text="Daily Work Hours:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(work_frame, textvariable=self.daily_hours_var).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(work_frame, text="Work Days per Week:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(work_frame, textvariable=self.work_days_var).grid(row=1, column=1, padx=10, pady=5)
        
        # Commute time
        commute_frame = ttk.LabelFrame(main_frame, text="Commute Time", padding=10)
        commute_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(commute_frame, text="One-way Commute (minutes):").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(commute_frame, textvariable=self.commute_minutes_var).grid(row=0, column=1, padx=10, pady=5)
        
        # Additional costs
        costs_frame = ttk.LabelFrame(main_frame, text="Additional Costs", padding=10)
        costs_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(costs_frame, text="Daily Additional Costs:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(costs_frame, textvariable=self.daily_costs_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(costs_frame, text="$").grid(row=0, column=2, sticky='w')
        
        # Calculate button
        ttk.Button(main_frame, text="Calculate", command=self.calculate).pack()
        
        # Results display area
        self.results_text = tk.Text(main_frame, height=10, width=60, state='disabled')
        self.results_text.pack(pady=20)
        
    def calculate(self):
        try:
            paycheck = self.paycheck_var.get()
            daily_hours = self.daily_hours_var.get()
            work_days = self.work_days_var.get()
            commute_minutes = self.commute_minutes_var.get()
            daily_costs = self.daily_costs_var.get()
            
            # Basic calculations
            weekly_work_hours = daily_hours * work_days
            daily_commute_hours = (commute_minutes * 2) / 60
            weekly_commute_hours = daily_commute_hours * work_days
            
            work_weeks_per_year = 50
            yearly_work_hours = weekly_work_hours * work_weeks_per_year
            yearly_commute_hours = weekly_commute_hours * work_weeks_per_year
            
            # Assume biweekly pay for now
            annual_income = paycheck * 26
            weekly_commute_costs = daily_costs * work_days
            yearly_commute_costs = weekly_commute_costs * work_weeks_per_year
            
            # Wage calculations
            traditional_wage = annual_income / yearly_work_hours if yearly_work_hours > 0 else 0
            net_yearly_income = annual_income - yearly_commute_costs
            total_committed_hours = yearly_work_hours + yearly_commute_hours
            true_wage = net_yearly_income / total_committed_hours if total_committed_hours > 0 else 0
            
            # Display results
            self.results_text.config(state='normal')
            self.results_text.delete(1.0, tk.END)
            
            results = f"""=== CALCULATION RESULTS ===

Traditional Hourly Wage: ${traditional_wage:.2f}
True Hourly Wage: ${true_wage:.2f}
Difference: ${traditional_wage - true_wage:.2f} per hour

Yearly Breakdown:
• Take-home pay: ${annual_income:,.2f}
• Commute costs: ${yearly_commute_costs:,.2f}
• Net income: ${net_yearly_income:,.2f}

Time Breakdown:
• Yearly work hours: {yearly_work_hours:.0f}
• Yearly commute hours: {yearly_commute_hours:.0f}
• Total committed hours: {total_committed_hours:.0f}
"""
            self.results_text.insert(1.0, results)
            self.results_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = TrueHourlyWageCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()