import contextvars

import psycopg2


def get_single_result(statement):
	with get_connection() as conn:
		with conn.cursor() as cur:
			cur.execute(statement)
			return cur.fetchone()


def get_connection():
	host = contextvars.ContextVar('HOST').get()
	port = contextvars.ContextVar('PORT').get()
	database = contextvars.ContextVar('DATABASE').get()
	user = contextvars.ContextVar('USER').get()
	password = contextvars.ContextVar('PASSWORD').get()

	return psycopg2.connect(
		host=host,
		port=port,
		database=database,
		user=user,
		password=password,
	)
