def calculate_true_hourly_wage():
    print("=== True Hourly Wage Calculator ===")
    print()
    
    # Get user input
    name = input("Enter your name: ")
    
    print("\n--- Pay Information ---")
    print("How often do you get paid?")
    print("1. Daily")
    print("2. Weekly")
    print("3. Bi-weekly (every 2 weeks)")
    print("4. Semi-monthly (twice a month)")
    print("5. Monthly")
    
    pay_frequency = input("\nEnter choice (1-5): ")
    
    paycheck_amount = float(input("Enter your take-home paycheck amount: $"))
    
    # Time inputs
    daily_commute_minutes = float(input("Enter your one-way commute time in minutes: "))
    daily_commute_miles = float(input("Enter your one-way commute distance in miles: "))
    daily_work_hours = float(input("Enter your daily work hours (excluding lunch): "))
    
    # Days per week
    work_days_per_week = float(input("How many days per week do you work? (e.g., 5): "))
    
    # Car-related inputs
    gas_mileage = float(input("Enter your car's gas mileage (miles per gallon): "))
    gas_price = float(input("Enter current gas price per gallon: $"))
    
    # Additional car costs
    print("\n--- Additional Cost Factors ---")
    print("For more accuracy, include estimated car maintenance and depreciation.")
    print("If unsure, you can use these estimates:")
    print("- IRS standard mileage rate (2024): $0.67/mile (includes all car costs)")
    print("- Or estimate maintenance/depreciation separately")
    print()
    
    use_irs_rate = input("Use IRS standard mileage rate for full cost? (yes/no): ").lower()
    
    if use_irs_rate == 'yes':
        irs_rate = 0.67  # 2024 IRS business mileage rate
        maintenance_per_mile = irs_rate - (gas_price / gas_mileage)
        print(f"Using full cost of ${irs_rate:.2f} per mile")
    else:
        maintenance_per_mile = float(input("Enter estimated maintenance/depreciation cost per mile (e.g., 0.15 for $0.15/mile): $"))
    
    # Transportation alternatives (optional)
    print("\n--- Alternative Transportation ---")
    print("Do you have any regular commuting costs besides driving?")
    has_other_costs = input("e.g., tolls, parking, public transit (yes/no): ").lower()
    
    daily_other_costs = 0
    if has_other_costs == 'yes':
        daily_other_costs = float(input("Enter daily additional commuting costs (tolls, parking, etc.): $"))
    
    print("\n" + "="*50)
    print(f"Calculating true hourly wage for {name}...")
    print("="*50)
    
    # Calculate annual income based on pay frequency
    print(f"\nConverting {pay_frequency} pay to annual income...")
    
    if pay_frequency == '1':  # Daily
        annual_income = paycheck_amount * work_days_per_week * 50  # 50 weeks/year
        pay_description = f"${paycheck_amount:.2f} per day"
        
    elif pay_frequency == '2':  # Weekly
        annual_income = paycheck_amount * 50  # 50 weeks/year
        pay_description = f"${paycheck_amount:.2f} per week"
        
    elif pay_frequency == '3':  # Bi-weekly (every 2 weeks)
        annual_income = paycheck_amount * 26  # 26 pay periods/year
        pay_description = f"${paycheck_amount:.2f} bi-weekly"
        
    elif pay_frequency == '4':  # Semi-monthly (twice a month)
        annual_income = paycheck_amount * 24  # 24 pay periods/year
        pay_description = f"${paycheck_amount:.2f} semi-monthly"
        
    elif pay_frequency == '5':  # Monthly
        annual_income = paycheck_amount * 12  # 12 months/year
        pay_description = f"${paycheck_amount:.2f} per month"
        
    else:
        print("Invalid choice, defaulting to bi-weekly")
        annual_income = paycheck_amount * 26
        pay_description = f"${paycheck_amount:.2f} bi-weekly"
    
    # Constants
    work_weeks_per_year = 50
    
    # Calculate commute costs and time
    daily_commute_hours = (daily_commute_minutes * 2) / 60  # Round trip
    round_trip_miles = daily_commute_miles * 2
    
    # Calculate various costs
    daily_fuel_cost = (round_trip_miles / gas_mileage) * gas_price
    daily_maintenance_cost = round_trip_miles * maintenance_per_mile
    daily_car_costs = daily_fuel_cost + daily_maintenance_cost + daily_other_costs
    
    # Weekly calculations
    weekly_commute_hours = daily_commute_hours * work_days_per_week
    weekly_work_hours = daily_work_hours * work_days_per_week
    weekly_car_costs = daily_car_costs * work_days_per_week
    
    # Yearly calculations
    yearly_work_hours = weekly_work_hours * work_weeks_per_year
    yearly_commute_hours = weekly_commute_hours * work_weeks_per_year
    yearly_car_costs = weekly_car_costs * work_weeks_per_year
    
    # Total time commitment (work + commute)
    total_yearly_hours_committed = yearly_work_hours + yearly_commute_hours
    
    # True hourly wage calculation
    net_yearly_income = annual_income - yearly_car_costs
    true_hourly_wage = net_yearly_income / total_yearly_hours_committed
    
    # Traditional hourly wage (just work hours)
    traditional_hourly_wage = annual_income / yearly_work_hours
    
    # After-cost hourly wage (work hours only, but with costs)
    after_cost_hourly_wage = net_yearly_income / yearly_work_hours
    
    # Display results
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    print(f"\nFor {name}:")
    print(f"Pay frequency: {pay_description}")
    print(f"Annual take-home income: ${annual_income:,.2f}")
    print(f"Traditional hourly wage: ${traditional_hourly_wage:.2f}")
    print(f"Hourly wage after costs: ${after_cost_hourly_wage:.2f}")
    print(f"TRUE hourly wage (including commute time): ${true_hourly_wage:.2f}")
    
    print("\n" + "="*50)
    print("COST BREAKDOWN")
    print("="*50)
    print(f"\nDaily Costs:")
    print(f"  Round trip: {round_trip_miles:.1f} miles")
    print(f"  Fuel: ${daily_fuel_cost:.2f}")
    print(f"  Maintenance/Depreciation: ${daily_maintenance_cost:.2f}")
    if daily_other_costs > 0:
        print(f"  Other (tolls/parking): ${daily_other_costs:.2f}")
    print(f"  TOTAL Daily: ${daily_car_costs:.2f}")
    
    print(f"\nYearly Costs ({work_weeks_per_year} weeks × {work_days_per_week} days/week):")
    print(f"  Fuel: ${daily_fuel_cost * work_days_per_week * work_weeks_per_year:,.2f}")
    print(f"  Maintenance/Depreciation: ${daily_maintenance_cost * work_days_per_week * work_weeks_per_year:,.2f}")
    if daily_other_costs > 0:
        print(f"  Other: ${daily_other_costs * work_days_per_week * work_weeks_per_year:,.2f}")
    print(f"  TOTAL Yearly: ${yearly_car_costs:,.2f}")
    
    print("\n" + "="*50)
    print("TIME BREAKDOWN")
    print("="*50)
    print(f"\nDaily:")
    print(f"  Work: {daily_work_hours:.1f} hours")
    print(f"  Commute: {daily_commute_hours:.1f} hours ({daily_commute_minutes} min each way)")
    print(f"  Total: {daily_work_hours + daily_commute_hours:.1f} hours")
    
    print(f"\nWeekly ({work_days_per_week} days):")
    print(f"  Work: {weekly_work_hours:.1f} hours")
    print(f"  Commute: {weekly_commute_hours:.1f} hours")
    print(f"  Total: {weekly_work_hours + weekly_commute_hours:.1f} hours")
    
    print(f"\nYearly ({work_weeks_per_year} weeks):")
    print(f"  Work: {yearly_work_hours:.0f} hours")
    print(f"  Commute: {yearly_commute_hours:.0f} hours")
    print(f"  Total committed time: {total_yearly_hours_committed:.0f} hours")
    
    print("\n" + "="*50)
    print("IMPACT ANALYSIS")
    print("="*50)
    
    # Percentage impacts
    wage_reduction_time = ((traditional_hourly_wage - true_hourly_wage) / traditional_hourly_wage) * 100
    wage_reduction_cost = ((traditional_hourly_wage - after_cost_hourly_wage) / traditional_hourly_wage) * 100
    time_vs_cost_impact = ((true_hourly_wage - after_cost_hourly_wage) / after_cost_hourly_wage) * 100
    
    print(f"\nImpact of costs alone: -${traditional_hourly_wage - after_cost_hourly_wage:.2f}/hr ({wage_reduction_cost:.1f}%)")
    print(f"Impact of commute time: -${after_cost_hourly_wage - true_hourly_wage:.2f}/hr ({time_vs_cost_impact:.1f}%)")
    print(f"Total impact: -${traditional_hourly_wage - true_hourly_wage:.2f}/hr ({wage_reduction_time:.1f}%)")
    
    # Calculate how much work time pays for commute
    hours_to_pay_for_daily_commute = daily_car_costs / (annual_income / yearly_work_hours / work_days_per_week)
    print(f"\nYou work {hours_to_pay_for_daily_commute:.2f} hours each day just to pay for your commute")
    
    # Per paycheck impact
    if pay_frequency == '3':  # Bi-weekly
        biweekly_commute_cost = daily_car_costs * work_days_per_week * 2
        biweekly_commute_hours = daily_commute_hours * work_days_per_week * 2
        print(f"\nPer Paycheck (Bi-weekly):")
        print(f"  Commute costs: ${biweekly_commute_cost:.2f}")
        print(f"  Commute time: {biweekly_commute_hours:.1f} hours")
        print(f"  That's {biweekly_commute_cost/paycheck_amount*100:.1f}% of your paycheck!")
    
    return true_hourly_wage


def quick_calculator():
    """A simpler version for quick calculations"""
    print("\n=== Quick Calculator (Bi-weekly Focus) ===")
    
    name = input("Your name: ")
    biweekly_pay = float(input("Bi-weekly take-home pay: $"))
    work_hours = float(input("Daily work hours: "))
    work_days_per_week = float(input("Days per week (e.g., 5): "))
    commute_minutes = float(input("One-way commute minutes: "))
    commute_miles = float(input("One-way commute miles: "))
    mpg = float(input("Car MPG: "))
    gas_price = float(input("Gas price per gallon: $"))
    
    # Quick calculations
    daily_commute_hours = commute_minutes * 2 / 60
    round_trip_miles = commute_miles * 2
    daily_fuel_cost = (round_trip_miles / mpg) * gas_price
    
    # Simple estimate
    daily_other_car_cost = round_trip_miles * 0.30  # $0.30/mile for other costs
    daily_total_cost = daily_fuel_cost + daily_other_car_cost
    
    # Annual calculations
    annual_income = biweekly_pay * 26
    weekly_work_hours = work_hours * work_days_per_week
    yearly_work_hours = weekly_work_hours * 50
    yearly_commute_hours = daily_commute_hours * work_days_per_week * 50
    yearly_costs = daily_total_cost * work_days_per_week * 50
    
    traditional_wage = annual_income / yearly_work_hours
    true_wage = (annual_income - yearly_costs) / (yearly_work_hours + yearly_commute_hours)
    
    # Per paycheck perspective
    biweekly_commute_cost = daily_total_cost * work_days_per_week * 2
    biweekly_commute_hours = daily_commute_hours * work_days_per_week * 2
    
    print(f"\n=== Results for {name} ===")
    print(f"Annual income: ${annual_income:,.2f}")
    print(f"Traditional wage: ${traditional_wage:.2f}/hr")
    print(f"True wage: ${true_wage:.2f}/hr")
    print(f"Difference: ${traditional_wage - true_wage:.2f}/hr")
    print(f"\nPer Bi-weekly Paycheck:")
    print(f"  Commute costs: ${biweekly_commute_cost:.2f}")
    print(f"  Commute time: {biweekly_commute_hours:.1f} hours")
    print(f"  Effective take-home: ${biweekly_pay - biweekly_commute_cost:.2f}")


def biweekly_focus_calculator():
    """Special calculator focused on bi-weekly pay"""
    print("\n=== Bi-weekly Pay True Wage Calculator ===")
    
    name = input("Enter your name: ")
    biweekly_pay = float(input("Enter your bi-weekly take-home pay: $"))
    work_days_per_week = float(input("How many days per week do you work? (e.g., 5): "))
    daily_work_hours = float(input("Enter your daily work hours: "))
    
    print("\n--- Commute Details ---")
    daily_commute_minutes = float(input("One-way commute time in minutes: "))
    daily_commute_miles = float(input("One-way commute distance in miles: "))
    
    print("\n--- Car Details ---")
    gas_mileage = float(input("Car's gas mileage (MPG): "))
    gas_price = float(input("Current gas price per gallon: $"))
    
    # Quick cost estimate
    print("\nUsing simplified cost estimate:")
    print("Fuel + $0.30/mile for maintenance/depreciation")
    
    # Calculations
    daily_commute_hours = daily_commute_minutes * 2 / 60
    round_trip_miles = daily_commute_miles * 2
    daily_fuel_cost = (round_trip_miles / gas_mileage) * gas_price
    daily_maintenance = round_trip_miles * 0.30
    daily_total_cost = daily_fuel_cost + daily_maintenance
    
    # Annual perspective
    annual_income = biweekly_pay * 26
    yearly_work_hours = daily_work_hours * work_days_per_week * 50
    yearly_commute_hours = daily_commute_hours * work_days_per_week * 50
    yearly_costs = daily_total_cost * work_days_per_week * 50
    
    # Bi-weekly perspective
    biweekly_commute_cost = daily_total_cost * work_days_per_week * 2
    biweekly_commute_hours = daily_commute_hours * work_days_per_week * 2
    biweekly_work_hours = daily_work_hours * work_days_per_week * 2
    
    # Wage calculations
    traditional_hourly = annual_income / yearly_work_hours
    net_annual_income = annual_income - yearly_costs
    true_hourly = net_annual_income / (yearly_work_hours + yearly_commute_hours)
    
    # Display
    print("\n" + "="*50)
    print(f"RESULTS FOR {name.upper()}")
    print("="*50)
    
    print(f"\nPAYCHECK ANALYSIS (Every 2 weeks):")
    print(f"  Take-home pay: ${biweekly_pay:.2f}")
    print(f"  Commute costs: -${biweekly_commute_cost:.2f}")
    print(f"  Effective pay: ${biweekly_pay - biweekly_commute_cost:.2f}")
    print(f"  Commute eats {biweekly_commute_cost/biweekly_pay*100:.1f}% of your paycheck")
    
    print(f"\nTIME ANALYSIS (Per Pay Period):")
    print(f"  Work time: {biweekly_work_hours:.1f} hours")
    print(f"  Commute time: {biweekly_commute_hours:.1f} hours")
    print(f"  Total: {biweekly_work_hours + biweekly_commute_hours:.1f} hours")
    
    print(f"\nHOURLY WAGES:")
    print(f"  Traditional: ${traditional_hourly:.2f}/hr")
    print(f"  True wage: ${true_hourly:.2f}/hr")
    print(f"  Difference: ${traditional_hourly - true_hourly:.2f}/hr")
    
    print(f"\nDAILY COMMUTE COST: ${daily_total_cost:.2f}")
    print(f"  Fuel: ${daily_fuel_cost:.2f}")
    print(f"  Other: ${daily_maintenance:.2f}")
    
    return true_hourly


# Main program
if __name__ == "__main__":
    print("TRUE HOURLY WAGE CALCULATOR")
    print("============================")
    print("Calculate your actual hourly wage including")
    print("commute time and costs")
    print()
    
    print("Choose calculator mode:")
    print("1. Full Calculator (all pay frequencies)")
    print("2. Quick Bi-weekly Calculator")
    print("3. Bi-weekly Focus Calculator")
    
    mode = input("\nEnter choice (1-3): ")
    
    try:
        if mode == "1":
            calculate_true_hourly_wage()
        elif mode == "2":
            quick_calculator()
        elif mode == "3":
            biweekly_focus_calculator()
        else:
            print("Invalid choice. Using bi-weekly focus.")
            biweekly_focus_calculator()
        
        # Ask if user wants to calculate again
        while True:
            again = input("\nCalculate again? (yes/no): ").lower()
            if again == 'yes':
                print("\nChoose mode: 1=Full, 2=Quick, 3=Bi-weekly Focus")
                mode = input("Enter choice: ")
                if mode == "1":
                    calculate_true_hourly_wage()
                elif mode == "2":
                    quick_calculator()
                else:
                    biweekly_focus_calculator()
            elif again == 'no':
                print("\nThank you for using the True Hourly Wage Calculator!")
                break
            else:
                print("Please enter 'yes' or 'no'")
                
    except ValueError:
        print("\nError: Please enter valid numbers for all inputs.")
    except ZeroDivisionError:
        print("\nError: Work hours cannot be zero.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")