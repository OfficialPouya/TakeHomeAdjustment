import sqlite3
from datetime import datetime
import json
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class CompensationData:
    """Data class to hold compensation information"""
    name: str
    salary: float
    rsu: float
    match_401k: float
    bonus_percent: float
    commute_time_minutes: float
    commute_distance_miles: float
    car_type: str
    fuel_cost: float
    car_cost: float
    car_mileage: float
    daily_hours: float
    gas_mileage: Optional[float] = None
    electric_efficiency: Optional[float] = None

class CompensationAnalyzer:
    def __init__(self, db_name="compensation_data.db"):
        """Initialize the analyzer with database connection"""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        """Create necessary database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compensation_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary REAL NOT NULL,
                rsu REAL NOT NULL,
                match_401k REAL NOT NULL,
                bonus_percent REAL NOT NULL,
                commute_time_minutes REAL NOT NULL,
                commute_distance_miles REAL NOT NULL,
                car_type TEXT NOT NULL,
                fuel_cost REAL NOT NULL,
                car_cost REAL NOT NULL,
                car_mileage REAL NOT NULL,
                daily_hours REAL NOT NULL,
                gas_mileage REAL,
                electric_efficiency REAL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                real_hourly_wage REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER,
                month_year TEXT,
                total_compensation REAL,
                commute_cost REAL,
                work_hours REAL,
                real_hourly_wage REAL,
                FOREIGN KEY (record_id) REFERENCES compensation_records (id)
            )
        ''')
        
        # Item cost analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id INTEGER,
                item_name TEXT NOT NULL,
                item_cost REAL NOT NULL,
                work_hours_needed REAL NOT NULL,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES compensation_records (id)
            )
        ''')
        
        self.conn.commit()
    
    def get_user_input(self):
        """Collect all necessary user input"""
        print("=== Compensation Analysis Tool ===")
        print()
        
        name = input("1. Enter your name: ").strip()
        
        salary = float(input("2. Enter your annual salary ($): "))
        rsu = float(input("3. Enter your RSU value (annual $): "))
        match_401k = float(input("4. Enter 401k match percentage (e.g., 4 for 4%): "))
        bonus_percent = float(input("5. Enter bonus percentage (e.g., 10 for 10%): "))
        
        commute_time_minutes = float(input("6. Enter average daily commute time (minutes): "))
        commute_distance_miles = float(input("7. Enter average daily commute distance (miles): "))
        
        print()
        print("8. Car Type:")
        print("   g - Gas car")
        print("   e - Electric car")
        car_type = input("   Enter your choice (g/e): ").strip().lower()
        
        if car_type == 'g':
            car_type = 'gas'
            fuel_cost = float(input("   Enter average gas price per gallon ($): "))
            gas_mileage = float(input("   Enter your car's gas mileage (miles per gallon): "))
            electric_efficiency = None
        else:
            car_type = 'electric'
            fuel_cost = float(input("   Enter average electricity cost per kWh ($): "))
            electric_efficiency = float(input("   Enter your car's efficiency (miles per kWh): "))
            gas_mileage = None
        
        car_cost_input = input("9. Enter car cost with mileage (format: 'cost,mileage' e.g., '30000,15000'): ")
        car_cost, car_mileage_total = map(float, car_cost_input.split(','))
        
        daily_hours = float(input("10. Enter average hours worked per day: "))
        
        return CompensationData(
            name=name,
            salary=salary,
            rsu=rsu,
            match_401k=match_401k,
            bonus_percent=bonus_percent,
            commute_time_minutes=commute_time_minutes,
            commute_distance_miles=commute_distance_miles,
            car_type=car_type,
            fuel_cost=fuel_cost,
            car_cost=car_cost,
            car_mileage=car_mileage_total,
            daily_hours=daily_hours,
            gas_mileage=gas_mileage,
            electric_efficiency=electric_efficiency
        )
    
    def calculate_commute_cost(self, data: CompensationData, work_days_per_year=260):
        daily_distance = data.commute_distance_miles * 2  # Round trip
        
        if data.car_type == 'gas':
            daily_gallons = daily_distance / data.gas_mileage
            daily_fuel_cost = daily_gallons * data.fuel_cost
        else:
            daily_kwh = daily_distance / data.electric_efficiency
            daily_fuel_cost = daily_kwh * data.fuel_cost
    
        cost_per_mile = data.car_cost / data.car_mileage
        daily_depreciation = daily_distance * cost_per_mile
        
        daily_total = daily_fuel_cost + daily_depreciation
        annual_commute_cost = daily_total * work_days_per_year
        
        return {
            'daily_fuel': daily_fuel_cost,
            'daily_depreciation': daily_depreciation,
            'daily_total': daily_total,
            'annual_total': annual_commute_cost
        }
    
    def calculate_real_hourly_wage(self, data: CompensationData):
        work_days_per_year = 260  # 52 weeks * 5 days
        bonus_amount = data.salary * (data.bonus_percent / 100)
        match_401k_amount = data.salary * (data.match_401k / 100)
        total_compensation = data.salary + data.rsu + bonus_amount + match_401k_amount
        commute_costs = self.calculate_commute_cost(data, work_days_per_year)
        annual_commute_cost = commute_costs['annual_total']
        daily_commute_hours = data.commute_time_minutes * 2 / 60
        total_daily_hours = data.daily_hours + daily_commute_hours
        annual_work_hours = total_daily_hours * work_days_per_year
        net_compensation = total_compensation - annual_commute_cost
        if annual_work_hours > 0:
            real_hourly_wage = net_compensation / annual_work_hours
        else:
            real_hourly_wage = 0
        
        if data.daily_hours > 0:
            annual_paid_hours = data.daily_hours * work_days_per_year
            nominal_hourly_wage = data.salary / annual_paid_hours
        else:
            nominal_hourly_wage = 0
        
        return {
            'total_compensation': total_compensation,
            'net_compensation': net_compensation,
            'annual_commute_cost': annual_commute_cost,
            'annual_work_hours': annual_work_hours,
            'annual_paid_hours': data.daily_hours * work_days_per_year,
            'real_hourly_wage': real_hourly_wage,
            'nominal_hourly_wage': nominal_hourly_wage,
            'commute_costs': commute_costs,
            'bonus_amount': bonus_amount,
            'match_401k_amount': match_401k_amount
        }
    
    def calculate_item_cost_in_hours(self, real_hourly_wage: float, item_cost: float, item_name: str = "") -> Dict[str, Any]:
        if real_hourly_wage <= 0:
            return {
                'hours': 0,
                'days': 0,
                'weeks': 0,
                'item_name': item_name,
                'item_cost': item_cost,
                'hourly_wage': real_hourly_wage
            }
        
        hours_needed = item_cost / real_hourly_wage
        work_days = hours_needed / 8  
        work_weeks = work_days / 5  
        
        return {
            'hours': hours_needed,
            'days': work_days,
            'weeks': work_weeks,
            'item_name': item_name,
            'item_cost': item_cost,
            'hourly_wage': real_hourly_wage
        }
    
    def analyze_item_purchase(self, record_id=None):
        """Analyze how many hours an item costs based on real hourly wage"""
        cursor = self.conn.cursor()
        
        if record_id is None:
            records = self.view_records()
            if not records:
                print("No records found. Please create a compensation record first.")
                return
            
            try:
                record_id = int(input("\nEnter the record ID to use for calculation: "))
            except ValueError:
                print("Invalid record ID.")
                return
        
        cursor.execute('SELECT name, real_hourly_wage FROM compensation_records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        
        if not record:
            print(f"Record ID {record_id} not found.")
            return
        
        name, real_hourly_wage = record
        print()
        print("="*60)
        print(f"ITEM COST ANALYSIS for {name}")
        print(f"Real Hourly Wage: ${real_hourly_wage:.2f}")
        print("="*60)
        
        while True:
            print()
            print("What would you like to analyze?")
            print("1. Single item purchase")
            print("2. Monthly subscription")
            print("3. Annual expense")
            print("4. View previous item analyses")
            print("5. Return to main menu")
            choice = input("\nEnter your choice (1-5): ").strip()
            if choice == '1':
                self._analyze_single_item(record_id, name, real_hourly_wage)
            elif choice == '2':
                self._analyze_monthly_subscription(record_id, name, real_hourly_wage)
            elif choice == '3':
                self._analyze_annual_expense(record_id, name, real_hourly_wage)
            elif choice == '4':
                self._view_item_analyses(record_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _analyze_single_item(self, record_id, name, real_hourly_wage):
        print()
        item_name = input("Enter the name of the item: ").strip()
        
        try:
            item_cost = float(input(f"Enter the cost of {item_name} ($): "))
        except ValueError:
            print("Invalid cost. Please enter a number.")
            return
        
        if item_cost <= 0:
            print("Item cost must be greater than 0.")
            return
        
        calculation = self.calculate_item_cost_in_hours(real_hourly_wage, item_cost, item_name)
        print()
        print("-" * 50)
        print(f"ITEM: {item_name}")
        print(f"COST: ${item_cost:.2f}")
        print(f"YOUR REAL HOURLY WAGE: ${real_hourly_wage:.2f}")
        print("-" * 50)
        print(f"This item costs you:")
        print(f"  {calculation['hours']:.2f} hours of work")
        print(f"  {calculation['days']:.2f} work days (8 hours/day)")
        print(f"  {calculation['weeks']:.2f} work weeks (5 days/week)")
        print("-" * 50)
        
        self._save_item_analysis(record_id, item_name, item_cost, calculation['hours'])
        compare = input("\nCompare with other time frames? (y/n): ").lower()
        if compare == 'y':
            self._display_time_comparisons(calculation['hours'])
    
    def _analyze_monthly_subscription(self, record_id, name, real_hourly_wage):
        print()
        subscription_name = input("Enter the name of the subscription: ").strip()
        
        try:
            monthly_cost = float(input(f"Enter the monthly cost of {subscription_name} ($): "))
        except ValueError:
            print("Invalid cost. Please enter a number.")
            return
        
        if monthly_cost <= 0:
            print("Monthly cost must be greater than 0.")
            return

        print()
        print("-" * 50)
        print(f"SUBSCRIPTION: {subscription_name}")
        print(f"MONTHLY COST: ${monthly_cost:.2f}")
        print(f"YOUR REAL HOURLY WAGE: ${real_hourly_wage:.2f}")
        print("-" * 50)
        monthly_hours = monthly_cost / real_hourly_wage
        print(f"Monthly cost requires: {monthly_hours:.2f} hours")
        annual_cost = monthly_cost * 12
        annual_hours = annual_cost / real_hourly_wage
        print(f"Annual cost (${annual_cost:.2f}) requires: {annual_hours:.2f} hours")
        daily_cost = monthly_cost / 30
        daily_hours = daily_cost / real_hourly_wage
        print(f"Daily cost (${daily_cost:.2f}) requires: {daily_hours:.2f} hours")
        print("-" * 50)
        self._save_item_analysis(record_id, f"{subscription_name} (Monthly)", monthly_cost, monthly_hours)
        self._save_item_analysis(record_id, f"{subscription_name} (Annual)", annual_cost, annual_hours)
    
    def _analyze_annual_expense(self, record_id, name, real_hourly_wage):
        print()
        expense_name = input("Enter the name of the annual expense: ").strip()
        
        try:
            annual_cost = float(input(f"Enter the annual cost of {expense_name} ($): "))
        except ValueError:
            print("Invalid cost. Please enter a number.")
            return
        
        if annual_cost <= 0:
            print("Annual cost must be greater than 0.")
            return
        
        calculation = self.calculate_item_cost_in_hours(real_hourly_wage, annual_cost, expense_name)
        print()
        print("-" * 50)
        print(f"ANNUAL EXPENSE: {expense_name}")
        print(f"ANNUAL COST: ${annual_cost:.2f}")
        print(f"YOUR REAL HOURLY WAGE: ${real_hourly_wage:.2f}")
        print("-" * 50)
        print(f"This annual expense costs you:")
        print(f"  {calculation['hours']:.2f} hours of work per year")
        print(f"  {calculation['days']:.2f} work days per year")
        print(f"  {calculation['weeks']:.2f} work weeks per year")
        monthly_cost = annual_cost / 12
        monthly_hours = monthly_cost / real_hourly_wage
        print(f"\nMonthly equivalent: ${monthly_cost:.2f} ({monthly_hours:.2f} hours/month)")
        print("-" * 50)
        self._save_item_analysis(record_id, expense_name, annual_cost, calculation['hours'])
    
    def _display_time_comparisons(self, hours_needed):
        print()
        print("TIME PERSPECTIVE:")
        print("-" * 40)
        
        movies = hours_needed / 2
        print(f"Equivalent to watching {movies:.1f} movies (2 hours each)")
        netflix_hours = 10 * 0.75  # 10 episodes * 45 minutes
        netflix_sessions = hours_needed / netflix_hours
        print(f"Equivalent to {netflix_sessions:.1f} Netflix binge sessions")
        
        gym_sessions = hours_needed
        print(f"Equivalent to {gym_sessions:.1f} gym sessions (1 hour each)")

        commutes = hours_needed
        print(f"Equivalent to {commutes:.1f} typical commutes (1 hour each)")
        print("-" * 40)
    
    def _save_item_analysis(self, record_id, item_name, item_cost, work_hours_needed):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO item_costs (record_id, item_name, item_cost, work_hours_needed)
            VALUES (?, ?, ?, ?)
        ''', (record_id, item_name, item_cost, work_hours_needed))
        
        self.conn.commit()
    
    def _view_item_analyses(self, record_id):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT item_name, item_cost, work_hours_needed, analysis_date
            FROM item_costs
            WHERE record_id = ?
            ORDER BY analysis_date DESC
        ''', (record_id,))
        
        items = cursor.fetchall()
        
        if not items:
            print("No item analyses found for this record.")
            return
        
        print()
        print("PREVIOUS ITEM ANALYSES:")
        print("-" * 80)
        print(f"{'Item':<30} {'Cost':<15} {'Hours Needed':<15} {'Date'}")
        print("-" * 80)
        
        total_hours = 0
        total_cost = 0
        
        for item in items:
            item_name, item_cost, hours_needed, date = item
            print(f"{item_name:<30} ${item_cost:<14.2f} {hours_needed:<14.2f} {date}")
            total_hours += hours_needed
            total_cost += item_cost
        
        print("-" * 80)
        print(f"{'TOTALS:':<30} ${total_cost:<14.2f} {total_hours:<14.2f}")
        print("-" * 80)
    
    def save_to_database(self, data: CompensationData, calculations: dict):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO compensation_records 
            (name, salary, rsu, match_401k, bonus_percent, commute_time_minutes, 
             commute_distance_miles, car_type, fuel_cost, car_cost, car_mileage, 
             daily_hours, gas_mileage, electric_efficiency, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.name, data.salary, data.rsu, data.match_401k, data.bonus_percent,
            data.commute_time_minutes, data.commute_distance_miles, data.car_type,
            data.fuel_cost, data.car_cost, data.car_mileage, data.daily_hours,
            data.gas_mileage, data.electric_efficiency, calculations['real_hourly_wage']
        ))
        
        record_id = cursor.lastrowid
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute('''
            INSERT INTO monthly_calculations 
            (record_id, month_year, total_compensation, commute_cost, work_hours, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            record_id, current_month, calculations['total_compensation'],
            calculations['annual_commute_cost'], calculations['annual_work_hours'],
            calculations['real_hourly_wage']
        ))
        
        self.conn.commit()
        return record_id
    
    def display_results(self, data: CompensationData, calculations: dict):
        print()
        print("="*60)
        print("COMPENSATION ANALYSIS RESULTS")
        print("="*60)
        print()
        print(f"Employee: {data.name}")
        print(f"Car Type: {data.car_type.upper()}")
        print()
        print("COMPENSATION BREAKDOWN:")
        print(f"   Base Salary: ${data.salary:,.2f}")
        print(f"   RSU: ${data.rsu:,.2f}")
        print(f"   Bonus ({data.bonus_percent}%): ${calculations['bonus_amount']:,.2f}")
        print(f"   401k Match ({data.match_401k}%): ${calculations['match_401k_amount']:,.2f}")
        print(f"   ------------------------------------")
        print(f"   TOTAL COMPENSATION: ${calculations['total_compensation']:,.2f}")
        print()
        print("COMMUTE COSTS (Annual):")
        print(f"   Daily Fuel: ${calculations['commute_costs']['daily_fuel']:.2f}")
        print(f"   Daily Depreciation: ${calculations['commute_costs']['daily_depreciation']:.2f}")
        print(f"   Daily Total: ${calculations['commute_costs']['daily_total']:.2f}")
        print(f"   Annual Commute Cost: ${calculations['annual_commute_cost']:,.2f}")
        print()
        print("TIME ANALYSIS:")
        print(f"   Daily Work Hours: {data.daily_hours:.1f}")
        daily_commute_hours = data.commute_time_minutes * 2 / 60
        print(f"   Daily Commute Hours: {daily_commute_hours:.1f}")
        print(f"   Total Daily Hours: {data.daily_hours + daily_commute_hours:.1f}")
        print(f"   Annual Paid Hours: {calculations['annual_paid_hours']:,.1f}")
        print(f"   Annual Total Hours (incl. commute): {calculations['annual_work_hours']:,.1f}")
        print()
        print("NET ANALYSIS:")
        print(f"   Net Compensation: ${calculations['net_compensation']:,.2f}")
        print(f"   REAL HOURLY WAGE (incl. commute): ${calculations['real_hourly_wage']:.2f}")
        print(f"   Nominal Hourly Wage (salary only): ${calculations['nominal_hourly_wage']:.2f}")
        difference = calculations['real_hourly_wage'] - calculations['nominal_hourly_wage']
        if calculations['nominal_hourly_wage'] > 0:
            difference_percent = (difference / calculations['nominal_hourly_wage']) * 100
        else:
            difference_percent = 0
        
        print()
        print("COMPARISON:")
        print(f"   Difference: ${difference:+.2f} ({difference_percent:+.1f}%)")
        print("="*60)
    
    def view_records(self):
        cursor = self.conn.cursor()     
        print()
        print("DATABASE RECORDS")
        print("-" * 80)
        
        cursor.execute('''
            SELECT id, name, created_date, real_hourly_wage, salary, rsu
            FROM compensation_records
            ORDER BY created_date DESC
        ''')
        
        records = cursor.fetchall()
        
        if not records:
            print("No records found in the database.")
            return
        
        for record in records:
            print(f"ID: {record[0]} | Name: {record[1]} | Date: {record[2]} | "
                  f"Real Hourly: ${record[3]:.2f} | Salary: ${record[4]:,.0f} | "
                  f"RSU: ${record[5]:,.0f}")
        
        return records
    
    def update_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM compensation_records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        
        if not record:
            print(f"Record ID {record_id} not found.")
            return
        
        print()
        print(f"Updating record for {record[1]}")
        print("Leave blank to keep current value.")
        print()
        salary = input(f"Current salary ${record[2]}: ") or record[2]
        rsu = input(f"Current RSU ${record[3]}: ") or record[3]
        daily_hours = input(f"Current daily hours {record[12]}: ") or record[12]

        cursor.execute('''
            UPDATE compensation_records 
            SET salary = ?, rsu = ?, daily_hours = ?
            WHERE id = ?
        ''', (float(salary), float(rsu), float(daily_hours), record_id))
        
        data = CompensationData(
            name=record[1],
            salary=float(salary),
            rsu=float(rsu),
            match_401k=record[4],
            bonus_percent=record[5],
            commute_time_minutes=record[6],
            commute_distance_miles=record[7],
            car_type=record[8],
            fuel_cost=record[9],
            car_cost=record[10],
            car_mileage=record[11],
            daily_hours=float(daily_hours),
            gas_mileage=record[13],
            electric_efficiency=record[14]
        )
        
        calculations = self.calculate_real_hourly_wage(data)
        cursor.execute('''
            UPDATE compensation_records 
            SET real_hourly_wage = ?
            WHERE id = ?
        ''', (calculations['real_hourly_wage'], record_id))

        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute('''
            INSERT INTO monthly_calculations 
            (record_id, month_year, total_compensation, commute_cost, work_hours, real_hourly_wage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            record_id, current_month, calculations['total_compensation'],
            calculations['annual_commute_cost'], calculations['annual_work_hours'],
            calculations['real_hourly_wage']
        ))
        
        self.conn.commit()
        print()
        print(f"Record {record_id} updated successfully!")
        
        return calculations
    
    def generate_report(self):
        """Generate a comprehensive report"""
        cursor = self.conn.cursor()
        print()
        print("COMPREHENSIVE REPORT")
        print("="*80)
        cursor.execute('''
            SELECT name, MAX(real_hourly_wage) as latest_wage, 
                   AVG(real_hourly_wage) as avg_wage, COUNT(*) as entries
            FROM compensation_records
            GROUP BY name
            ORDER BY latest_wage DESC
        ''')
        
        results = cursor.fetchall()
        print()
        print()
        print("REAL HOURLY WAGE SUMMARY:")
        print("-" * 60)
        for name, latest, avg, entries in results:
            print(f"{name:20} Latest: ${latest:7.2f} | Avg: ${avg:7.2f} | Entries: {entries}")
        if results:
            cursor.execute('''
                SELECT c.name, m.month_year, m.real_hourly_wage
                FROM monthly_calculations m
                JOIN compensation_records c ON m.record_id = c.id
                WHERE c.name = ?
                ORDER BY m.month_year
            ''', (results[0][0],))
            
            trends = cursor.fetchall()
            
            if trends:
                print()
                print(f"MONTHLY TREND for {trends[0][0]}:")
                print("-" * 40)
                for name, month, wage in trends:
                    print(f"  {month}: ${wage:.2f}")
        
        print()
        print("="*80)
    def close(self):
        self.conn.close()

def main():
    analyzer = CompensationAnalyzer()
    
    while True:
        print()
        print("="*60)
        print("COMPENSATION ANALYSIS TOOL")
        print("="*60)
        print("1. Enter new compensation data")
        print("2. View all records")
        print("3. Update existing record")
        print("4. Analyze item purchase cost")
        print("5. Generate report")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            data = analyzer.get_user_input()
            calculations = analyzer.calculate_real_hourly_wage(data)
            record_id = analyzer.save_to_database(data, calculations)
            analyzer.display_results(data, calculations)
            print()
            print(f"Record saved with ID: {record_id}")
            
        elif choice == '2':
            analyzer.view_records()
            
        elif choice == '3':
            records = analyzer.view_records()
            if records:
                try:
                    record_id = int(input("\nEnter record ID to update: "))
                    calculations = analyzer.update_record(record_id)
                    
                    if calculations:
                        show = input("\nShow updated results? (y/n): ").lower()
                        if show == 'y':
                            cursor = analyzer.conn.cursor()
                            cursor.execute('SELECT * FROM compensation_records WHERE id = ?', (record_id,))
                            record = cursor.fetchone()
                            
                            data = CompensationData(
                                name=record[1],
                                salary=record[2],
                                rsu=record[3],
                                match_401k=record[4],
                                bonus_percent=record[5],
                                commute_time_minutes=record[6],
                                commute_distance_miles=record[7],
                                car_type=record[8],
                                fuel_cost=record[9],
                                car_cost=record[10],
                                car_mileage=record[11],
                                daily_hours=record[12],
                                gas_mileage=record[13],
                                electric_efficiency=record[14]
                            )
                            analyzer.display_results(data, calculations)
                except ValueError:
                    print("Invalid record ID.")
                    
        elif choice == '4':
            analyzer.analyze_item_purchase()
            
        elif choice == '5':
            analyzer.generate_report()
            
        elif choice == '6':
            analyzer.close()
            print()
            print("Thank you for using the Compensation Analysis Tool!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()