from kadi_apy import KadiManager
import bibtexparser
from datetime import datetime, timezone


def convert_names(authors_string):
    # Split the input string by " and "
    authors = authors_string.split(" and ")
    
    # Process each author
    formatted_authors_identifier = []
    formatted_authors_names = []
    for author in authors:
        # Split each author by comma and strip any leading/trailing spaces
        parts_identifier = [part.strip() for part in author.replace(",", "").split()]
        parts_names = [part.strip() for part in author.split(",")]
        # Join the parts with an underscore
        formatted_author = "_".join(parts_identifier)
        formatted_authors_identifier.append(formatted_author)
        formatted_author = " ".join(parts_names)
        formatted_authors_names.append(formatted_author)
    
    return formatted_authors_identifier, formatted_authors_names


manager = KadiManager()


def get_publication_date_metadata(pub_year):

  new_year = datetime(int(pub_year), 1, 1, 0, 0, 0)

  # Format the date and time in the desired format
  formatted_time = new_year.strftime("%Y-%m-%dT%H:%M:%S%z")

  # Since the offset is not specified, manually add the timezone offset if needed
  # For UTC+00:00
  formatted_time += "+00:00"

  publication_date_metadata = {
    "key": "publicationDate",
    "type": "date",
    "validation": {
      "required": True
    },
    "value": formatted_time
  }

  return publication_date_metadata


def get_creation_date_metadata():

    now = datetime.now(timezone.utc)

    # Format the date and time in the desired format
    formatted_datetime = now.isoformat()

    creation_date_metadata = {
      "description": "Date of the creation of document. Can be identical to the date of the creation of the record if no better date is known.",
      "key": "creationDate",
      "type": "date",
      "validation": {
        "required": True
      },
      "value": formatted_datetime
    }

    return creation_date_metadata


def get_language_metadata(lang = "english"):

    language_metadata = {
      "description": "Language of the document.",
      "key": "language",
      "type": "str",
      "validation": {
        "required": True
      },
      "value": lang
    }

    return language_metadata


def get_doi_metadata(doi = ""):

    doi_metadata = {
      "key": "doi",
      "type": "str",
      "value": doi
    }

    return doi_metadata


def get_pages_metadata(pages = ""):

    pages_metadata = {
      "key": "pages",
      "type": "str",
      "value": pages
    }

    return pages_metadata


def get_journal_metadata(jounral = ""):

    journal_metadata = {
      "key": "journalName",
      "type": "str",
      "value": jounral
    }

    return journal_metadata


with open('../bin/reference.bib', 'r') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for entry in bib_database.entries:

    author_identifiers, author_names = convert_names(entry['author'])
    author_id = []
    
    # Obtain the author names and create records for authors if they already don't exist
    for author_identifier, author_name in zip(author_identifiers, author_names):
        try:
            author_record = manager.record(identifier=author_identifier)
            author_id.append(author_record.id)
        except Exception as err:
            author_record = manager.record(identifier=author_identifier, title=author_name, create=True, type="person")
            author_id.append(author_record.id)
        
    # Create publication identifier from the publication title    
    bib_identifier = entry['title'].replace(" ", "_")

    # Create a record for the publication
    bib_record = manager.record(identifier=bib_identifier, title=entry['title'], create=True, type="publication")

    # Add the creation date, language, publication date, doi, pages and journal name are metadata 
    bib_record.add_metadata(get_creation_date_metadata(), force=True) 
    bib_record.add_metadata(get_language_metadata(), force=True)
    bib_record.add_metadata(get_publication_date_metadata(entry['year']), force=True)
    try: 
      bib_record.add_metadata(get_doi_metadata(entry['doi']), force=True)
    except Exception as err:
        pass
    bib_record.add_metadata(get_pages_metadata(entry['pages']), force=True)
    bib_record.add_metadata(get_journal_metadata(entry['journal']), force=True)

    # Link the publication record to the author records
    for id, author_name in zip(author_id, author_names):
      bib_record.link_record(id, name=bib_identifier + '_' + author_name)




