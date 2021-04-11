import sys
import names
import random

import uuid
import xlsxwriter

from faker import Faker

fake = Faker()


def progressBar(current, total, barLength=20):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * barLength - 1) + '>'
    spaces = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%, count: %d' %
          (arrow, spaces, percent, current), end='\r')


if len(sys.argv) < 2:
    print('Please insert the count as program argument.')
    exit(1)

loopCount = int(sys.argv[1])

workbook = xlsxwriter.Workbook('dataLoadFile.xlsx')
worksheet = workbook.add_worksheet()

for i in range(loopCount):
    genderId = random.randint(1, 2)

    genderInd = 'male'
    if genderId == 2:
        genderInd = 'female'

    worksheet.write(i, 0, str(uuid.uuid4()))
    worksheet.write(i, 1, names.get_first_name(gender=genderInd))
    worksheet.write(i, 2, names.get_first_name())
    worksheet.write(i, 3, names.get_last_name())
    worksheet.write(i, 4, fake.date_of_birth(minimum_age=18, maximum_age=60))
    worksheet.write(i, 5, random.randint(1001, 9999))
    if genderId == 1:
        worksheet.write(i, 6, 'M')
    else:
        worksheet.write(i, 6, 'F')
    worksheet.write(i, 7, random.randint(1111111111, 9999999999))

    progressBar(i, loopCount, 100)

workbook.close()

print('Processing Completed Sucessfully.')
