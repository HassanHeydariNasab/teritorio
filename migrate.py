from playhouse.migrate import *
migrator = SqliteMigrator(db)
migrator = MySQLMigrator(db)
migrator = PostgresqlMigrator(db)
migrate(migrator.add_column('parto', 'minajxo', minajxo),)

migrate(migrator.drop_column('parto', 'materialo'),)
migrate(migrator.add_column('parto', 'materialo', materialo),)