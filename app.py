# from tasks import ola_mundo

# ola_mundo.delay()


from dataclasses import dataclass
from celery import chain

from tasks import ocr_documento, validar_cpf_governo

@dataclass
class Pessoa:
    nome: str
    telefone: str
    documento: str

def cadastro(pessoa: Pessoa):
    chain(
        ocr_documento.s(pessoa.documento),
        validar_cpf_governo.s(),
        # enviar_email
    )()

    return 'Cadastro em avaliação, você receberá um email em breve'


p = Pessoa('Eduardo', '8398714758', 'images/documento_certo.png')

cadastro(p)

