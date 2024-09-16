import csv
from datetime import datetime, timedelta
from database_manager import Session, User, AccessEvent



def log_event(employee_id, event_type):
    timestamp = datetime.now()
    with open('employee_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([employee_id, event_type, timestamp])

def calculate_hours_worked(employee_id, date):
    total_time = timedelta()
    with open('employee_log.csv', mode='r') as file:
        reader = csv.reader(file)
        entries = [row for row in reader if row[0] == employee_id and row[2].startswith(date)]
        
       
        for i in range(0, len(entries), 2):
            entry_time = datetime.fromisoformat(entries[i][2])
            if i+1 < len(entries):
                exit_time = datetime.fromisoformat(entries[i+1][2])
                total_time += exit_time - entry_time
    
    return total_time

def generate_report(employee_id, start_date, end_date):
    current_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    report = {}
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        hours_worked = calculate_hours_worked(employee_id, date_str)
        report[date_str] = hours_worked
        current_date += timedelta(days=1)
    
    return report

if __name__ == "__main__":
    log_event("12345", "entry")
    log_event("12345", "exit")

    today = datetime.now().strftime('%Y-%m-%d')
    hours_worked = calculate_hours_worked("12345", today)
    print(f"Ore lucrate azi: {hours_worked}")

    start_date = "2024-08-01"
    end_date = "2024-08-18"
    report = generate_report("12345", start_date, end_date)
    print("Raport ore lucrate:")
    for date, hours in report.items():
        print(f"{date}: {hours}")

def calculate_daily_hours():
    session = Session()
    today = datetime.now().date()
    report_date_str = today.strftime('%Y-%m-%d')

    chiulangii = []
    
    for user in session.query(User).all():
        total_worked = timedelta()
        events = session.query(AccessEvent).filter(
            AccessEvent.person_id == user.id,
            AccessEvent.timestamp.between(today, today + timedelta(days=1))
        ).order_by(AccessEvent.timestamp).all()

        if events:
            for i in range(0, len(events), 2):
                if i+1 < len(events):
                    total_worked += events[i+1].timestamp - events[i].timestamp
            
            if total_worked < timedelta(hours=8):
                chiulangii.append((user.first_name + " " + user.last_name, total_worked))