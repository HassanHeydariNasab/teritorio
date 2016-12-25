migrator = SqliteMigrator(db)
migrate(migrator.add_column('Model', 'field', field),)
