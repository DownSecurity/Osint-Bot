#Dev by DownSecurity no skid pls :/
#Discord : downsecurity
#Github : DownSecurity

#Import
import discord
import os
import subprocess
import time
import aiohttp
import asyncio
import threading
import requests
import fake_useragent

#From
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
from datetime import datetime, timedelta


#Config Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='prefix', intents=intents)
bot.remove_command('help')
bot_owner_id = owner_id #Owner Id

# Pour les commandes modération
def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

#Event Ready
@bot.event
async def on_ready():
    print(f'=========================================')
    print(f'== Connecté en tant que {bot.user.name}  ==')
    print(f'============ Coded By DownSec ===========')
    print(f'=========================================')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("&help || downsecurity")) #Status et Activté

#Event "commande erreur"
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Commande non reconnue. Tapez '&help osint' pour la liste des commandes disponibles.")
        
        
        
#Commande Change Pfp (bot)       
@bot.command()
async def changepfp(ctx):
    if ctx.author.id != bot_owner_id:
        await ctx.send("Seul l'administrateur du bot peut utiliser cette commande.")
        return
    if not ctx.message.attachments:
        await ctx.send("Veuillez joindre une image avec la commande.")
        return
    attachment = ctx.message.attachments[0]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await bot.user.edit(avatar=image_data)
                    await ctx.send("Photo de profil changée avec succès.")
                else:
                    await ctx.send(f"Erreur lors de la récupération de l'image. Statut {resp.status}")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite : {e}")

        
# Commande Github
@bot.command()
async def github(ctx, username):
    api_url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': 'token kzjbOg3iOm4k4MRpBss76yxlZSPJtoOPaqxirsfX'}
   
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login')
            avatar_url = user_data.get('avatar_url')
            created_at = user_data.get('created_at')
            repos_count = user_data.get('public_repos')
            email = user_data.get('email', 'Non disponible')
            # NE PAS TOUCHER sinon la cmd va plus marcher
            embed = discord.Embed(title=f'<<:emoji_1159589442982518886:1186116002983989338> // GitHub Info - {username}', color=0x000000)
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name='<:user:1185311277766160567> Username', value=username, inline=True)
            embed.add_field(name='<:avatar:1186113205043466280> Avatar', value=f'[Cliquez ici]({avatar_url})', inline=True)
            embed.add_field(name='<:creation:1186113203072139366> Date de création du compte', value=created_at, inline=False)
            embed.add_field(name='<:repo:1185311282157584456> Nombre de repo', value=repos_count, inline=True)
            embed.add_field(name='<:email:1185311203480842321> Email', value=email, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Erreur lors de la requête à l\'API GitHub. Code d\'état : {response.status_code}')
    except Exception as e:
        await ctx.send(f'Erreur : {e}')    
        
        
# Commandes Change Pfp (Serveur)
@bot.command()
async def changepfp2(ctx):
    if ctx.author.id != bot_owner_id:
        await ctx.send("Seul l'administrateur du bot peut utiliser cette commande.")
        return
    if ctx.message.attachments:
        image_url = ctx.message.attachments[0].url

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    image_data = await response.read()
            await ctx.guild.edit(icon=image_data)
            await ctx.send('PDP du serveur mise à jour avec succès!')
        except Exception as e:
            await ctx.send(f'Erreur : {e}')
    else:
        await ctx.send('Veuillez joindre une image à la commande.')
        
        
        
# Commande Phone        
@bot.command()
async def phone(ctx, phone_number):
    try:
        phone_number = phone_number.lstrip('+')
        if not phone_number.isdigit():
            await ctx.send("Veuillez fournir un numéro de téléphone valide.")
            return
        
        # NE PAS TOUCHER c'est le lien vers l'api sans sa la cmd marche plus !!
        api_url = f'http://apilayer.net/api/validate?access_key=1cf3dd77bf1ad472dedd792814d7da7c&number={phone_number}'
        response = requests.get(api_url)
        data = response.json()
        print(data)
        if 'valid' in data:
            if data['valid']:
                embed = discord.Embed(
                    title=f"<:emoji_1159574364438667315:1185311272724603053> / Phone Informations - {phone_number}",
                    color=0x000000
                )
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Numéro", value=data['number'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Format local", value=data['local_format'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Format international", value=data['international_format'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Préfixe du pays", value=data['country_prefix'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Code pays", value=data['country_code'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Nom du pays", value=data['country_name'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Localisation", value=data['location'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Opérateur", value=data['carrier'], inline=False)
                embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Type de ligne", value=data['line_type'], inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Le numéro de téléphone {phone_number} n'est pas valide.")
        else:
            await ctx.send(f"La réponse de l'API n'a pas le format attendu.")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors de la recherche des informations pour le numéro de téléphone {phone_number}.\n{str(e)}")

        

# COmmande Cdump pour crée le dossier database  
@bot.command()
async def cdb(ctx):
    if not os.path.exists("database"):
        os.makedirs("database")
        await ctx.send("Le dossier 'database' a été créé avec succès.")
    else:
        await ctx.send("Le dossier 'database' existe déjà.")
        
        

# Commande Ip    
@bot.command()
async def ip(ctx, ip_address):
    # NE pAS TOUCHER c'est le lien de l'api sa
    ip_info_url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(ip_info_url)
    ip_info_data = response.json()
    embed = discord.Embed(title=f"<:emoji_1176895835246694440:1185311241728704705> / Ip Informations - {ip_address}", color=0x000000)
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Ip", value=ip_info_data.get('ip', 'N/A'), inline=False)
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Pays", value=ip_info_data.get('country', 'N/A'), inline=True)
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Région", value=ip_info_data.get('region', 'N/A'), inline=True)
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Ville", value=ip_info_data.get('city', 'N/A'), inline=True)
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Opérateurs", value=ip_info_data.get('org', 'N/A'), inline=False)
    loc = ip_info_data.get('loc', '').split(',')
    if len(loc) == 2:
        latitude, longitude = loc
        embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - Adresse Approximative", value=f"{latitude}, {longitude}", inline=True)
    vpn_status = "Oui" if ip_info_data.get('vpn') else "Non"
    embed.add_field(name="<:emoji_1170088049317793832:1185311199647244379> - VPN", value=vpn_status, inline=True)
    await ctx.send(embed=embed)        
        
        

# Comande Help    
@bot.command()
async def help(ctx, category=None):
    if category is None:
        embed = discord.Embed(title='Commandes disponibles', description='Liste des catégories de commandes du bot :')
        embed.add_field(name='&help osint', value='Commandes liées à l\'osint', inline=False)
        embed.set_footer(text='Bot by downsec')
        await ctx.send(embed=embed)
    else:
        if category.lower() == 'osint':
            embed = discord.Embed(title='Commandes OSINT', description='Liste des commandes OSINT :')
            embed.add_field(name='&lookup <valeur> (marchent pas avec les email)', value='Rechercher une valeur dans la base de données.', inline=False)
            embed.add_field(name='&db_add <fichier>', value='Ajoute des fichiers à la base de données.', inline=False)
            embed.add_field(name='&scrap <cfx>', value='Sert a scrap une db.', inline=False)
            embed.add_field(name='&github <pseudo>', value='Sert a avoir des informations sur un github.', inline=False)
            embed.add_field(name='&ip <ip>', value='Sert a avoir des info sur une ip.', inline=False)
            embed.add_field(name='&phone <numero tout coller sans le +>', value='Sert a avoir des info sur un numéro de tel.', inline=False)
            embed.set_footer(text='Bot by downsec')
            await ctx.send(embed=embed)
        else:
            await ctx.send("Catégorie invalide. Les catégories disponibles sont : osint, modération, ...")



#Commande WhiteList
@bot.command()
async def wl(ctx, user: discord.User):
    category_id = 1187385847528558672  # Mettre l'id de votre categorie
    category = ctx.guild.get_channel(category_id)
    channel_name = f"{user.name}"
    channel = await ctx.guild.create_text_channel(channel_name, category=category)
    await channel.set_permissions(user, read_messages=True, send_messages=True)
    await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    await ctx.send(f"Le salon {channel.mention} a été créé et est visible uniquement par {user.mention}.")

            

#Commande Lookup
@bot.command()
async def lookup(ctx, search_term):
    await ctx.send("Recherche lancée, Veuillez patienter.")
    if not os.path.exists("database"):
        await ctx.send("Le dossier 'database' n'existe pas.")
        return

    async def run_search():
        try:
            with open(f"{search_term}.txt", "w") as file:
                subprocess.call(['grep', '-r', '-h', search_term, 'database'], stdout=file)
        except subprocess.CalledProcessError as e:
            result = f"Erreur lors de la recherche : {e.output}"
        with open(f"{search_term}.txt", "a") as file:
            file.write('''
               ,   ,
             ,-`{-`/
          ,-~ , \\ {-~~-,
        ,~  ,   ,`,-~~-,`,
      ,`   ,   { {      } }                                             }/
     ;     ,--/`\\ \\    / /                                     }/      /,/
    ;  ,-./      \\ \\  { {  (                                  /,;    ,/ ,/
    ; /   `       } } `, `-`-.___                            / `,  ,/  `,/
     \|         ,`,`    `~.___,---}                         / ,`,,/  ,`,;
      `        { {                                     __  /  ,`/   ,`,;
            /   \\ \\                                 _,`, `{  `,{   `,`;`
           {     } }       /~\\         .-:::-.     (--,   ;\\ `,}  `,`;
           \\\\._./ /      /` , \\      ,:::::::::,     `~;   \\},/  `,`;     ,-=-
            `-..-`      /. `  .\\_   ;:::::::::::;  __,{     `/  `,`;     {
                       / , ~ . ^ `~`\\:::::::::::<<~>-,,`,    `-,  ``,_    }
                    /~~ . `  . ~  , .`~~\\:::::::;    _-~  ;__,        `,-`
           /`\\    /~,  . ~ , '  `  ,  .` \\::::;`   <<<~```   ``-,,__   ;
          /` .`\\ /` .  ^  ,  ~  ,  . ^   .   , ` .`-,___,---,__            ``
         / ` , ,`\\.  ` ~  ,  ^ ,  `  ~ . . ``~~~`,                   `   ``
        /` ~ . ~ \\ , ` .  ^  `  , . ^   .   , ` .`-,___,---,__            ``
      /` ` . ~ . ` \\ `  ~  ,  .  ,  `  ,  . ~  ^  ,  .  ~  , .`~---,___
    /` . `  ,  . ~ , \\  `  ~  ,  .  ^  ,  ~  .  `  ,  ~  .  ^  ,  ~  .  `-,


    Coded by downsecurity
    ''')
        await ctx.send(file=discord.File(f"{search_term}.txt"))
        await asyncio.sleep(10)
        os.remove(f"{search_term}.txt")
    loop = asyncio.get_event_loop()
    task = loop.create_task(run_search())
    await task



#Commande Useribfo
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(title=f"Informations sur l'utilisateur {member.display_name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Nom d'utilisateur", value=member.name, inline=False)
    embed.add_field(name="Discriminateur", value=member.discriminator, inline=False)
    embed.add_field(name="Surnom", value=member.display_name, inline=False)
    embed.add_field(name="Date de création du compte", value=member.created_at, inline=False)
    await ctx.send(embed=embed)    



# Commande Db_Add
@bot.command()
async def db_add(ctx):
    print("Nouvelle tentative d'ajout")
    attachments = ctx.message.attachments
    if not attachments:
        await ctx.send('Aucun fichier joint. Utilisez &db_add avec des fichiers joints.')
        return
    db_add_folder = 'database'
    os.makedirs(db_add_folder, exist_ok=True)
    await ctx.message.delete()
    for attachment in attachments:
        file_path = os.path.join(db_add_folder, attachment.filename)
        await attachment.save(file_path)
    await ctx.send(f'Fichiers ajoutés avec succès !')

    
#Dans les string (c'est sa les string : "") vous metez le token de votre bot   
bot.run("token_bot")
