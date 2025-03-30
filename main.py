import xml.etree.ElementTree as ET
import datetime
import json

try:
    spec = json.load(open('data.json', encoding='utf-8'))
except:
    # Copy data.example.json to data.json with cp or copy
    with open('data.example.json','r', encoding='utf-8') as source:
        with open('data.json', 'w', encoding='utf-8') as destination:
            destination.writelines(source.readlines())

    print('data.json created. Edit it and run again.')
    exit(0)

current_weight = spec['weight']
start_date = datetime.datetime.strptime(spec['start_date'], "%Y-%m-%d").date()
habits = spec['habits'][:10]

# Open SVG file
svg_file = ET.parse("template.svg")
root = svg_file.getroot()

# Update weights and dates
for i in range(1, 13):
    weight_id = f"peso{i}"
    weight_tspan = root.find(f".//*[@id='{weight_id}']")
    if not type(weight_tspan) == type(None):
        weight_tspan.text = str(current_weight + 6 - i)
    else:
        print(f"No weight element found for weight {i}")


for i in range(1,16):
    date_id = f"date{i}"
    date_tspan = root.find(f".//*[@id='{date_id}']")
    if not type(date_tspan) == type(None):
        date = start_date + datetime.timedelta(days=(i-1)*7)
        date_tspan.text = date.strftime("%d/%m")
    else:
        print(f"No date element found for day {i*7}")


# Update subtitle
subtitle_tspan = root.find(".//*[@id='subtitle']")
if not type(subtitle_tspan) == type(None):
    habits_str = "|".join(f"{h['emoji']} {h['habit']}" for h in habits)
    subtitle_tspan.text = habits_str
else:
    print("No subtitle element found")


# Update habits
for i in range(len(habits)):
    habit_id = f"habit{i+1}"
    habit_tspan = root.find(f".//*[@id='{habit_id}']")
    if not type(habit_tspan) == type(None):
        habit_tspan.text = habits[i]["emoji"]
    else:
        print(f"No habit element found for {habit_id}")


# Save updated SVG file
svg_file.write(f"habit-tracker-{str(start_date)}.svg")
print("Sheet created!")
