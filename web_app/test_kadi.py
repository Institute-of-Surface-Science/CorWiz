# from kadi_apy import KadiManager
# import bibtexparser


# manager = KadiManager()

# with open('../bin/reference_test.bib', 'r') as bibtex_file:
#     bib_database = bibtexparser.load(bibtex_file)

# for entry in bib_database.entries:
        
#     # Create publication identifier from the publication title    
#     bib_identifier = entry['title'].replace(" ", "_")

#     # Create a record for the publication
#     bib_record = manager.record(identifier=bib_identifier)

#     table_id = bib_record.get_file_id('tables.xlsx')
#     bib_record.download_file(table_id, '../bin/temp/tables.xlsx')

import pandas as pd
df = pd.read_excel('../bin/atmospheric_corrosion_model_kadi_identifiers.xlsx')
print(df.iloc[:, 0].tolist())