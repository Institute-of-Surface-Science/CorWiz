from kadi_apy import KadiManager

manager = KadiManager()

# Retrieve an existing record by its ID.
# template = manager.template(id=19)

# record = manager.record()

# print(record.id)


# record = manager.record(
#     identifier="new_Rec",
#     title="My template",
#     create=True,
#     type="Document"
# )

meta_data = {
    "key": "language",
    "type": "str",
    "validation": {
      "required": True
    },
    "value": "English"
    }

record = manager.record(id=55)

record.add_metadata(meta_data, force=True)

# record.save()


# record.delete()

# record.export('lol', export_type='json', pipe=False)