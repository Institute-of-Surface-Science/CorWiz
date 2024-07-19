import tabula


file_name = 'Korrosion_und_Korrosionsschutz_1_Korrosion_von_Met..._----_(DIN_EN_ISO_9223_).pdf'
page_no = 13
data = tabula.read_pdf('../bin/documents/' + file_name, pages=page_no)
print(data)
tabula.convert_into('../bin/documents/' + file_name, '../bin/output/tables/' + file_name + '_' + 'page_' + str(page_no) + '.csv', output_format='csv', pages=page_no)