import os
import csv
from shutil import move
from datetime import datetime
from database_manager import Session, AccessEvent

def process_csv_files(directory='intrari'):
    session = Session()
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            with open(os.path.join(directory, filename), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    event = AccessEvent(
                        person_id=int(row[0]),
                        gate_id=int(filename.split('Poarta')[1].split('.')[0]),
                        direction=row[1],
                        timestamp=datetime.fromisoformat(row[2])
                    )
                    session.add(event)
                session.commit()
            move(os.path.join(directory, filename), os.path.join('backup_intrari', filename))

if __name__ == '__main__':
    process_csv_files()