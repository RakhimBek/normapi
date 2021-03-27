import psycopg2

from jproperties import Properties


def get_single_result(statement):
	with get_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(statement)
			return cur.fetchone()


def get_connection():
	properties = Properties()
	with open("environment.properties", "rb") as f:
		properties.load(f, "utf-8")

	return psycopg2.connect(
		host=properties.get('HOST').data,
		port=int(properties.get('PORT').data),
		database=properties.get('DATABASE').data,
		user=properties.get('USER').data,
		password=properties.get('PASSWORD').data
	)
