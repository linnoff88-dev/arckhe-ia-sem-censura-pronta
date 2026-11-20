#!/usr/bin/env python3
"""Conversa com um modelo local em uma instância própria do Ollama. Python 3.10+."""
import argparse
import contextlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
VERSION = '1.0.0'

class KitError(Exception):
    pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise KitError('O runtime tentou redirecionar a conexão. Operação interrompida.')

def profile():
    try:
        cfg = json.loads((ROOT / 'perfil.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise KitError('Não foi possível ler perfil.json: ' + str(exc)) from exc
    name = cfg.get('modelo', '')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?(?::[A-Za-z0-9_.-]+)?', name):
        raise KitError('Nome de modelo inválido. Use nome local, nunca URL.')
    if 'cloud' in name.lower():
        raise KitError('Modelos cloud não são aceitos por este kit.')
    if type(cfg.get('porta_runtime')) is not int or not 1024 <= cfg['porta_runtime'] <= 65535:
        raise KitError('porta_runtime precisa ser um inteiro entre1024 e65535.')
    if type(cfg.get('contexto')) is not int or not 512 <= cfg['contexto'] <= 8192:
        raise KitError('contexto precisa ficar entre512 e8192.')
    if type(cfg.get('max_tokens')) is not int or not 1 <= cfg['max_tokens'] <= 2048:
        raise KitError('max_tokens precisa ficar entre1 e2048.')
    return cfg

def free_port(port):
    with socket.socket() as s:
        try:
            s.bind(('127.0.0.1', port))
        except OSError as exc:
            raise KitError(f'Porta {port} ocupada. Encerre a outra execução deste kit; não vamos usar um serviço desconhecido.') from exc

def stop_process(process):
    if process is None:
        return
    if os.name == 'posix':
        # O grupo é exclusivo do filho iniciado com start_new_session=True.
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
    elif process.poll() is None:
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
        process.wait(timeout=10)

class Runtime:
    def __init__(self, cfg):
        self.cfg = cfg
        self.base = f"http://127.0.0.1:{cfg['porta_runtime']}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        self.process = None
        self.log = None
        self.binary = shutil.which('ollama')
        self.env = {k:v for k,v in os.environ.items() if not k.startswith('OLLAMA_')}
        # Reuse only an explicit model storage path; no inherited remote hosts or debug logging.
        if os.environ.get('OLLAMA_MODELS'):
            self.env['OLLAMA_MODELS'] = os.environ['OLLAMA_MODELS']
        self.env.update(OLLAMA_HOST=self.base, OLLAMA_NO_CLOUD='1', OLLAMA_MAX_LOADED_MODELS='1',
                        OLLAMA_NUM_PARALLEL='1', OLLAMA_CONTEXT_LENGTH=str(cfg['contexto']), OLLAMA_KEEP_ALIVE='120s')

    def request(self, path, data=None, timeout=30):
        if path not in ('/api/version', '/api/tags', '/api/show', '/api/chat', '/api/generate'):
            raise KitError('Rota não permitida.')
        body = None if data is None else json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(self.base + path, data=body, headers={'Content-Type':'application/json'})
        try:
            with self.opener.open(req, timeout=timeout) as res:
                raw = res.read(4 * 1024 * 1024 + 1)
            if len(raw) > 4 * 1024 * 1024:
                raise KitError('Resposta acima do limite de4MB.')
            return json.loads(raw)
        except urllib.error.HTTPError as exc:
            raise KitError(f'Ollama retornou HTTP{exc.code}. Consulte .estado/runtime.log.') from exc
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise KitError('Não foi possível conversar com o runtime local: ' + str(exc)) from exc

    def __enter__(self):
        if not self.binary:
            raise KitError('Ollama não encontrado. Instale pelo https://ollama.com/download e abra um novo terminal.')
        free_port(self.cfg['porta_runtime'])
        state = ROOT / '.estado'
        state.mkdir(mode=0o700, exist_ok=True)
        self.log = (state / 'runtime.log').open('w', encoding='utf-8')
        args = dict(env=self.env, stdout=self.log, stderr=subprocess.STDOUT)
        if os.name == 'posix':
            args['start_new_session'] = True
        else:
            args['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP
        try:
            self.process = subprocess.Popen([self.binary, 'serve'], **args)
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if self.process.poll() is not None:
                    raise KitError('Runtime não iniciou. Consulte .estado/runtime.log.')
                try:
                    self.request('/api/version', timeout=1)
                    if self.process.poll() is not None:
                        raise KitError('A instância própria encerrou durante a inicialização.')
                    return self
                except KitError:
                    time.sleep(0.2)
            raise KitError('O runtime não ficou pronto em30s. Consulte .estado/runtime.log.')
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def __exit__(self, *args):
        stop_process(self.process)
        if self.log:
            self.log.close()
        self.process = None

    def ensure_model(self):
        selected = self.cfg['modelo']
        tags = self.request('/api/tags').get('models', [])
        found = next((m for m in tags if m.get('name') == selected or m.get('model') == selected), None)
        if not found:
            raise KitError(f'Modelo {selected} ainda não foi preparado. Execute: python3 ia.py preparar')
        meta = self.request('/api/show', {'model': selected})
        if meta.get('remote_host') or meta.get('remote_model') or found.get('remote_host'):
            raise KitError('Este modelo aponta para processamento remoto. O kit exige pesos locais.')
        if not isinstance(found.get('size'), int) or found['size'] <= 0:
            raise KitError('O modelo não apresenta tamanho local válido.')
        expected = self.cfg.get('digest_esperado')
        actual = str(found.get('digest', '')).removeprefix('sha256:')
        if expected and actual != expected:
            raise KitError(f'O modelo mudou de digest. Esperado: {expected}. Encontrado: {actual}. Confira a página oficial do modelo antes de decidir atualizar digest_esperado em perfil.json; se não puder confirmar, não prossiga.')
        return found

    def prepare(self):
        print('Baixando ou conferindo pesos do modelo:', self.cfg['modelo'], flush=True)
        try:
            subprocess.run([self.binary, 'pull', self.cfg['modelo']], env=self.env, check=True, timeout=3600)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise KitError('Preparação interrompida. Confira internet e espaço em disco; rode preparar novamente.') from exc
        info = self.ensure_model()
        print('Modelo local preparado. Digest:', info.get('digest'))

    def chat(self, messages, max_tokens=None):
        response = self.request('/api/chat', {
            'model': self.cfg['modelo'], 'messages': messages, 'stream': False,
            'keep_alive': self.cfg.get('keep_alive', '120s'),
            'options': {'num_ctx': self.cfg['contexto'], 'num_predict': max_tokens or self.cfg['max_tokens'],
                        'temperature': self.cfg['temperatura']},
            **({'think': False} if self.cfg.get('desativar_pensamento') else {})
        }, timeout=600)
        text = response.get('message', {}).get('content')
        if not isinstance(text, str) or not text.strip():
            raise KitError('O modelo não devolveu resposta de texto. Não vamos tratar saída vazia como sucesso.')
        return text.strip(), response

    def unload(self):
        # A ausência de prompt solicita somente descarregar o modelo, não gera outra resposta.
        with contextlib.suppress(KitError):
            self.request('/api/generate', {'model':self.cfg['modelo'], 'keep_alive':0}, timeout=30)

def initial_messages(cfg):
    return [{'role':'system', 'content':cfg['sistema']}]

def get_question(args):
    if args.arquivo:
        data = args.arquivo.read_text(encoding='utf-8')
    elif args.texto:
        data = args.texto
    else:
        data = sys.stdin.read()
    if not data.strip():
        raise KitError('Digite uma pergunta, use --arquivo ou forneça texto pela entrada padrão.')
    if len(data) > 12000:
        raise KitError('Entrada acima de12000caracteres. Envie um trecho menor para o contexto configurado.')
    return data

def verify(rt):
    info = rt.ensure_model()
    messages = initial_messages(rt.cfg)
    messages.append({'role':'user', 'content':'Quanto é 17 mais 25? Responda somente com o número.'})
    text, raw = rt.chat(messages, max_tokens=64)
    ok = bool(re.fullmatch(r'\s*42[.!]?\s*', text))
    receipt = {'versao_kit':VERSION, 'quando':time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'modelo':rt.cfg['modelo'],
               'digest':info.get('digest'), 'runtime':rt.base, 'nuvem_desativada':True,
               'ferramentas_externas':False, 'resposta_teste':text, 'teste_17_mais_25':ok,
               'interfaces_rede':[name for _,name in socket.if_nameindex()],
               'namespace_somente_loopback':set(name for _,name in socket.if_nameindex())=={'lo'},
               'tokens_gerados':raw.get('eval_count'), 'inferencia_real':True,
               'limite':'Confirma este caso de resposta local; não é auditoria do sistema operacional nem prova de ausência de recusas.'}
    dest = ROOT / '.estado/verificacao.json'
    dest.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if ok else 1

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--versao', action='version', version=VERSION)
    sub = ap.add_subparsers(dest='comando', required=True)
    sub.add_parser('diagnostico', help='confere requisitos sem carregar modelo')
    sub.add_parser('preparar', help='baixa os pesos pela internet; não conversa com modelo')
    sub.add_parser('conversar', help='abre conversa no terminal; /sair encerra')
    sub.add_parser('verificar', help='executa pergunta real e salva recibo local')
    ask = sub.add_parser('perguntar', help='responde uma pergunta real')
    ask.add_argument('texto', nargs='?')
    ask.add_argument('--arquivo', type=Path)
    args = ap.parse_args(argv)
    try:
        cfg = profile()
        if args.comando == 'diagnostico':
            print(json.dumps({'kit':cfg['nome'], 'python':sys.version.split()[0], 'ollama':shutil.which('ollama'),
                              'modelo':cfg['modelo'], 'ram_recomendada_gb':cfg['ram_recomendada_gb'],
                              'porta_exclusiva':cfg['porta_runtime'], 'nuvem':'desativada pelo kit',
                              'proxima_acao':'preparar (com internet) ou verificar (modelo já baixado)'}, ensure_ascii=False, indent=2))
            return 0 if shutil.which('ollama') else 2
        question = get_question(args) if args.comando == 'perguntar' else None
        with Runtime(cfg) as rt:
            try:
                if args.comando == 'preparar':
                    rt.prepare()
                    return 0
                rt.ensure_model()
                if args.comando == 'verificar':
                    return verify(rt)
                if args.comando == 'perguntar':
                    messages = initial_messages(cfg) + [{'role':'user', 'content':question}]
                    print(rt.chat(messages)[0])
                    return 0
                print(cfg['nome'] + ' · modelo ' + cfg['modelo'])
                print('Conversa local, sem histórico salvo. /limpar reinicia e /sair encerra.')
                messages = initial_messages(cfg)
                while True:
                    try:
                        text = input('\nVocê: ').strip()
                    except EOFError:
                        break
                    if text == '/sair':
                        break
                    if text == '/limpar':
                        messages = initial_messages(cfg)
                        print('Conversa reiniciada.')
                        continue
                    if not text:
                        continue
                    if len(text)>12000:
                        print('Mensagem longa demais; envie até12000caracteres.')
                        continue
                    # Keep only a few turns; context is bounded by the configured runtime.
                    messages = initial_messages(cfg) + messages[1:][-6:]
                    messages.append({'role':'user', 'content':text})
                    answer, _ = rt.chat(messages)
                    print('\nIA: ' + answer)
                    messages.append({'role':'assistant', 'content':answer})
                return 0
            finally:
                if args.comando != 'preparar':
                    rt.unload()
    except KeyboardInterrupt:
        print('\nConversa encerrada.', file=sys.stderr)
        return 130
    except (KitError, OSError) as exc:
        print('Erro: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
