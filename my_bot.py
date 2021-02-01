import discord
from discord import Member
from discord.ext import commands
from banco import *
import random



client = commands.Bot(command_prefix= '.')

conn = creat_conn()


@client.event
async def on_ready():
    print("Bot está pronto")
 

@client.command()
async def cria(ctx, *arg):
	nome = ''
	for i in range(len(arg)):
		if i == 0:
			nome += arg[i]
		else:
			nome += ' '+ arg[i]
	await ctx.send(f'Criando ficha - Personagem = {nome} no usuário {ctx.author.name}')
	cria_ficha(conn,[nome,ctx.author.id])

@client.command()
async def deleta(ctx, *arg):
	nome = ''
	for i in range(len(arg)):
		if i == 0:
			nome += arg[i]
		else:
			nome += ' '+ arg[i]
	if del_ficha(conn,nome,ctx.author.id):
		del_ficha(conn,nome,ctx.author.id)
		await ctx.send(f'Deletando ficha - Personagem = {nome} no usuário {ctx.author.name}')
	else:
		await ctx.send(f'Falha ao deletar, nome inválido!')



@client.command()
async def usar(ctx, *arg):
	nome = ''
	for i in range(len(arg)):
		if i == 0:
			nome += arg[i]
		else:
			nome += ' '+ arg[i]
	sel_ficha(conn,nome,ctx.author.id)
	await ctx.send(f'Selecionando ficha para uso - Personagem = {nome} no usuário {ctx.author.name}')





@client.command()
async def minhasfichas(ctx):
	fichas = loc_fichas(conn,str(ctx.author.id))
	nomes = []
	print(fichas)
	print(type(fichas[0]))
	print(fichas[0][0])
	for i in range(len(fichas)):
		row = []
		print(fichas[i][1])
		if fichas[i][1]:
			row.append('X')
		else:
			row.append(' ')
		print(fichas[i][2])
		row.append(fichas[i][2])
		row.append(fichas[i][3])
		print(row)
		nomes.append(row)
	grad = 'Suas fichas são -----------------------\nUsando | Personagem | Level\n'

	for i in range(len(nomes)):
		grad += '[{}]  | {}  | {} \n'.format(nomes[i][0],nomes[i][1],nomes[i][2])

	await ctx.send(grad)

@client.command()
async def j(ctx, *arg):
	for d in arg:
		if d[0].lower() == 'd' and d[1:].isnumeric():
			print(d[1:]) 
			await ctx.send(f'{ctx.author.name} tirou com D{d[1:]} = {random.randint(1,int(d[1:]))}')
		elif d[0].isnumeric() and d[1].lower() == 'd' and d[2:].isnumeric():
			for i in range(int(d[0])):
				await ctx.send(f'{ctx.author.name} tirou com D{d[2:]} = {random.randint(1,int(d[2:]))}')


@client.command()
async def ficha(ctx, *arg):
	nome = ''
	if arg:
		for i in range(len(arg)):
			if i == 0:
				nome += arg[i]
			else:
				nome += ' '+ arg[i]
	else:
		nome = per_em_uso(conn,str(ctx.author.id))
	data = ficha_loc(conn,nome,str(ctx.author.id))
	print(data)
	print("seu conteudo é " , data)
	x = 'Não'
	if data[0][1]:
		x = 'Sim'

	await ctx.send(f"Nome = {data[0][2]}\nFicha em uso = [{x}]\nLevel = {data[0][3]}\nXp = {data[0][16]}\nPróximo Lv = {data[0][3]*400}\nForça = {data[0][4]}\nLuta = {data[0][5]}\nPrecisão = {data[0][6]}\nDestreza = {data[0][7]}\nVigor = {data[0][8]}\nIntelecto = {data[0][9]}\nCarisma = {data[0][10]}\nPontos de Vida = {data[0][11]}\nDeslocamento = {data[0][12]}\nEsquiva = {data[0][13]}\nIniciativa = {data[0][14]}\nMoedas = {data[0][15]}")


@client.command()
async def up (ctx, *arg):
	for d in arg:
		if d.lower() == 'level':
			up_atr(conn,'level',str(ctx.author.id))

	await ctx.send(f'Level up...')

@client.command()
async def xp(ctx, *arg):
	xp = arg[0]
	per = per_em_uso(conn,str(ctx.author.id))
	if arg[0].isnumeric():
		new_xp = xp_add(conn,xp,str(ctx.author.id))
	await ctx.send(f"Xp do {per} = {new_xp}")


@client.command()
async def edit(ctx,*arg):
	per = per_em_uso(conn,str(ctx.author.id))
	if arg[0].lower() == "ajuda":
		await ctx.send(f"""Comandos .edit para alterar dados da ficha:{per}:\n
							Inserir os valores desejados no lugar dos \*\*\* \n
							.edit nome \*\*\* - Para mudar o nome do personagem\n
							.edit alguma \*\*\* - Pra fazer algo""")
	elif arg[0].lower() == "nome":
		nome = ""
		for i in range(1,len(arg)):
			if i == 1:
				nome += arg[i]
			else:
				nome += ' '+ arg[i]
		print(nome)
		alter(conn,"nome",str(nome),str(ctx.author.id))
		await ficha(ctx)

	else:
		alter(conn,arg[0].lower(),arg[1],str(ctx.author.id))
		await ficha(ctx)


client.run('NzY1NTc0MDg4NzU5ODM2NzIz.X4Wybg.STv-VnKA1kJxsjElUeBAHAu20H0')