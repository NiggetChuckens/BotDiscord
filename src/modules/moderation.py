

async def clear(ctx, amount: int = 1):
    if amount > 50: await ctx.send("No puedes borrar más de 50 mensajes a la vez.")
    await ctx.channel.purge(limit=amount + 1)