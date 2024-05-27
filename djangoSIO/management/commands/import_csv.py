"""class Command(BaseCommand):
    help = 'Importa dados do CSV para o modelo Product'

    def handle(self, *args, **kwargs):
        arquivo_csv = 'comprasPedroTeixeira.csv'  # Certifique-se de que o nome do arquivo CSV está correto
        with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            for linha in leitor:
                #verificar se é a primeira linha e se for ele cria uma invoice
    

                #)
        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
"""
