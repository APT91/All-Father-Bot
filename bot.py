import os, sqlite3, discord, colorama
from discord.ext import commands

#Configure Bot Information
admins = ['YOUR DISCORD ID HERE']
token = 'YOUR BOT TOKEN'
bot = commands.Bot(command_prefix='?', intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    con = sqlite3.connect('odin.db')
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, user_id INTEGER, status TEXT)')
    con.commit()
    cur.close()
    con.close()

    os.system('clear')
    print(colorama.Fore.GREEN + '[!] Bot is online...')
    

#Help Command
@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(title='All Father', color=discord.Color.dark_embed())
    embed.add_field(name='?search <Discord ID>', value='Use this command to search the database.', inline=False)
    embed.add_field(name='?about', value='Get developer information.')
    await ctx.send(embed=embed)

#About Information
@bot.command(name='about')
async def about(ctx):
    embed = discord.Embed(title='Developer Information', color=discord.Color.dark_embed())
    embed.add_field(name='Author', value='APT91', inline=False)
    embed.add_field(name='Version', value='1.0.0', inline=False)
    embed.add_field(name='Donate', value='BTC: [I need to add my address!]', inline=False)
    await ctx.send(embed=embed)

##ADMIN COMMANDS##
@bot.command(name='adduser')
async def add_user(ctx, username, user_id, status):
    if ctx.author.id in admins:
        con = sqlite3.connect('odin.db')
        cur = con.cursor()
        cur.execute('INSERT INTO users(username, user_id, status) VALUES (?, ?, ?)', (username, user_id, status))
        con.commit()
        cur.close()
        con.close()

        await ctx.send("User has been added!")
        print(colorama.Fore.GREEN + "[+] New user in database!")
    else:
        await ctx.send("You do not have access to that command!")

@bot.command(name='deluser')
async def del_user(ctx, user_id):
    if ctx.author.id in admins:
        con = sqlite3.connect('odin.db')
        cur = con.cursor()
        cur.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        con.commit()
        cur.close()
        con.close()

        await ctx.send("User has been deleted!")
        print(colorama.Fore.RED + "[-] User removed from database!")
    else:
        await ctx.send("You do not have access to that command!")

@bot.command(name='edituser')
async def edit_user(ctx, user_id, status):
    if ctx.author.id in admins:
        con = sqlite3.connect('odin.db')
        cur = con.cursor()
        cur.execute('UPDATE users SET status = ? WHERE user_id = ?', (status, user_id,))
        con.commit()
        cur.close()
        con.close()

        await ctx.send("User has been updated!")
        print(colorama.Fore.YELLOW + "[*] User has been updated!")
    else:
        await ctx.send("You do not have access to that command!")

##User Commands##
@bot.command(name='search')
async def search(ctx, user_id):
    con = sqlite3.connect('odin.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = cur.fetchone()

    if result:
        embed = discord.Embed(title='Search Results', color=discord.Color.dark_embed())
        embed.add_field(name='Username', value=result[0], inline=False)
        embed.add_field(name='User ID', value=result[1], inline=False)
        embed.add_field(name='Status', value=result[2], inline=False)

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Search Results', color=discord.Color.dark_embed())
        embed.add_field(name='No results found!', value='User may not exist or is not in our database!')

        await ctx.send(embed=embed)


bot.run(token)
