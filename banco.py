import psycopg2
import pyexpat


def creat_conn():
	try:
		conn = psycopg2.connect(user = 'xcsujnweporffc',
								password = '1335a83ca739b52f79773d92e70fc44a7daf578dbaf6804616c1d5ca7434800d',
								host = "ec2-35-168-54-239.compute-1.amazonaws.com",
                                port = "5432",
                                database = "dd810u3tdm5rq6")
	except Error as e:
		print(e)
	
	return conn

def cria_ficha(conn,ficha):
	sql = "INSERT INTO fichas(nome, id_discord_user, level, forca, luta, precisao, destreza, vigor, intelecto, carisma, pontos_de_vida, deslocamento, esquiva, iniciativa, moedas) VALUES(%s,%s,1,1,1,1,1,1,1,1,1,1,1,1,0); "
	cur = conn.cursor()
	cur.execute(sql,ficha)
	conn.commit()
	return cur.lastrowid

def loc_fichas(conn,user):
	cur = conn.cursor()
	print(user)
	cur.execute("SELECT * FROM fichas WHERE id_discord_user=%s ORDER BY level DESC;",(user,))
	return cur.fetchall()


def del_ficha(conn,nome,user):
	cur = conn.cursor()
	cur.execute("DELETE FROM fichas WHERE nome=%s  AND id_discord_user=%s;",(nome,str(user),))
	conn.commit()
	return True


def sel_ficha(conn,nome,user):
	cur = conn.cursor()
	cur.execute("UPDATE fichas SET ficha_em_uso = 'f' WHERE id_discord_user=%s;",(str(user),))
	cur.execute("UPDATE fichas SET ficha_em_uso = 't' WHERE id_discord_user=%s and nome=%s;",(str(user),nome,))
	conn.commit()

def ficha_loc(conn,nome,user):
	cur = conn.cursor()
	cur.execute("SELECT * FROM fichas WHERE nome=%s AND id_discord_user=%s;",(nome,user,))
	data = cur.fetchall()
	return data

def up_atr(conn,atr,user):
	cur = conn.cursor()
	sql = "SELECT {} FROM fichas WHERE ficha_em_uso=\'t\' AND id_discord_user=\'{}\';".format(atr,user)
	print(sql)
	cur.execute(sql)
	level = int(cur.fetchall()[0][0]) + 1
	sql = "UPDATE fichas SET {}={} WHERE id_discord_user=%s AND ficha_em_uso=\'t\';".format(atr,str(level))
	cur.execute(sql,(user,))
	conn.commit()

def xp_add(conn,xp,user):
	cur = conn.cursor()
	sql = "SELECT xp FROM fichas WHERE ficha_em_uso=\'t\' AND id_discord_user=\'{}\';".format(user)
	cur.execute(sql)
	current_xp = cur.fetchall()[0][0]
	sql = "UPDATE fichas SET xp = {} WHERE ficha_em_uso=\'t\' AND id_discord_user=\'{}\'".format((int(current_xp)+int(xp)),user)
	cur.execute(sql)
	conn.commit()
	return (int(current_xp)+int(xp))

def alter(conn,atr,value,user):
	cur = conn.cursor()
	sql = "UPDATE fichas SET {} = \'{}\' WHERE ficha_em_uso=\'t\' AND id_discord_user=\'{}\';".format(atr,value,user)
	cur.execute(sql)
	conn.commit()

def per_em_uso(conn,user):
	cur = conn.cursor()
	sql = "SELECT nome from fichas WHERE ficha_em_uso=\'t\' AND id_discord_user=\'{}\';".format(user)
	cur.execute(sql)
	nome = cur.fetchall()[0][0]
	return nome