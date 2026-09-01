import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

materiais = [
    "Cobre",
    "Prata",
    "Electro",
    "Ouro",
    "Platina"
]

# 1. Lógica de cálculo
def converter_moeda(moeda_origem, moeda_destino, quantidade):
    valores_em_cobre = {
        'cobre': 1,
        'prata': 10,
        'electro': 50,
        'ouro': 100,
        'platina': 1000
    }
    
    origem = moeda_origem.lower()
    destino = moeda_destino.lower()
    
    total_em_cobre = int(quantidade * valores_em_cobre[origem])
    
    resultado = int(total_em_cobre // valores_em_cobre[destino])
    resto_em_cobre = total_em_cobre % valores_em_cobre[destino]
    sobra_moeda_origem = resto_em_cobre // valores_em_cobre[origem]
    return resultado, sobra_moeda_origem

# 2. Configuração do cliente Discord
class MeuBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincroniza os slash commands globalmente com o Discord
        await self.tree.sync()

bot = MeuBot()

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user} (ID: {bot.user.id})")

# 3. Slash Command (/calcular)
@bot.tree.command(name="calcular", description="Executa o cálculo personalizado")
@app_commands.describe(
    moeda_origem="Moeda de origem",
    quantidade="Quantidade",
    moeda_destino="Moeda de destino"
)
async def calcular(interaction: discord.Interaction, moeda_origem: str, quantidade: int, moeda_destino: str):
    try:
        resultado, sobra_moeda_origem = converter_moeda(moeda_origem, moeda_destino, quantidade)
        await interaction.response.send_message(
            f"**Resultado:** Suas ***{quantidade}*** moedas de {moeda_origem.capitalize()} equivalem a ***{resultado}*** moedas de {moeda_destino.capitalize()}.\n**Sobra:** Sobraram {sobra_moeda_origem} moedas de {moeda_origem.capitalize()}."
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ **Erro no cálculo:** {str(e)}", 
            ephemeral=True
        )

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("BOT-TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)