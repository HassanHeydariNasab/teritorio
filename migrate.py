from playhouse.migrate import *
migrator = SqliteMigrator(db)
migrator = MySQLMigrator(db)
migrate(migrator.add_column('parto', 'minajxo', minajxo),)
