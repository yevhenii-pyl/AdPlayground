import csv

input_file = 'data/ad_events.csv'
output_file = 'data/ad_events_fixed.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    # В заголовку з TargetingCriteria одна колонка, так що все норм
    writer.writerow(header)

    for row in reader:
        # Якщо рядок довший за заголовок — треба виправити
        if len(row) > len(header):
            # Визначимо позицію TargetingCriteria в заголовку
            target_idx = header.index('TargetingCriteria')

            # Візьмемо всі частини TargetingCriteria до AdSlotSize (адже після 5-ї колонки маємо 3 частини)
            # Тут ми знаємо, що TargetingCriteria розбито на 3 окремі колонки
            # Тобто обʼєднаємо їх у один рядок з комами
            targeting_parts = row[target_idx:target_idx+3]
            targeting = ', '.join(part.strip() for part in targeting_parts)

            # Побудуємо новий рядок:
            # Візьмемо все до TargetingCriteria
            fixed_row = row[:target_idx]
            # Додамо обʼєднане TargetingCriteria
            fixed_row.append(targeting)
            # Додамо решту колонок, починаючи з позиції TargetingCriteria+3
            fixed_row.extend(row[target_idx+3:len(header)])

            writer.writerow(fixed_row)
        else:
            writer.writerow(row)
