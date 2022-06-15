from celery import Celery
from httpx import post, get
from celery.contrib import rdb
from base64 import standard_b64encode

app = Celery(
    broker='pyamqp://guest@localhost:49154'

)


@app.task
def ola_mundo():
    return 'Olá, Mundo'

@app.task(
    name='Texto do documento',
    bind=True,
    retry_backoff=True,
    autoretry_for=(ValueError,)
)
def ocr_documento(self, documento):
    documento = open(documento, 'rb').read()

    image = standard_b64encode(documento).decode('utf-8')
    
    data = {
        'image': image 
    }

    response = post(
        'https://live-159-external.herokuapp.com/document-to-text-choice',
        json=data,
        timeout=None

    )
    if response.status_code == 200:
        return response.json()
    raise ValueError('Deu Erro')


class CPFError(BaseException):
    ...


@app.task(
    bind=True,
    autoretry_for=(CPFError,)
)
def validar_cpf_governo(self, cpf):
    if isinstance(cpf, dict):
        cpf = cpf['cpf']
    response = get(
        f'https://live-159-external.herokuapp.com/check-cpf?cpf={cpf}',
        timeout=None
    )
    # rdb.set_trace()
    if response.status_code == 200:
        return response.json()['cpf-status']
    raise CPFError('Erro no cpf!')

