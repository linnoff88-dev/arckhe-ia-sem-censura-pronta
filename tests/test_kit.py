import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import threading
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ia', ROOT/'ia.py');ia=importlib.util.module_from_spec(spec);spec.loader.exec_module(ia)
class LocalServer(BaseHTTPRequestHandler):
    mode='normal'
    received=[]
    def log_message(self,*args):pass
    def do_GET(self):
        if self.mode=='redirect':
            self.send_response(302);self.send_header('Location','http://example.invalid/leak');self.end_headers();return
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers()
        if self.path=='/api/tags':
            body={'models':[{'name':'local:tag','size':1234,'digest':'sha256:abc'}]}
        else:body={'version':'test'}
        self.wfile.write(json.dumps(body).encode())
    def do_POST(self):
        body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.received.append((self.path,body))
        self.send_response(200);self.end_headers()
        if self.path=='/api/show':
            out={'remote_host':'provider.invalid'} if self.mode=='remote' else {}
        else:out={'message':{'content':'' if self.mode=='empty' else '42'},'eval_count':1}
        self.wfile.write(json.dumps(out).encode())

class KitTests(unittest.TestCase):
    def setUp(self):
        LocalServer.mode='normal';LocalServer.received=[]
        self.server=HTTPServer(('127.0.0.1',0),LocalServer)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.cfg={'modelo':'local:tag','porta_runtime':self.server.server_port,'contexto':2048,'max_tokens':64,'temperatura':0.2,'sistema':'teste','digest_esperado':'abc'}
        self.rt=ia.Runtime(self.cfg)
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
    def test_local_model_real_http_contract(self):
        self.assertEqual(self.rt.ensure_model()['size'],1234)
    def test_reject_remote_model(self):
        LocalServer.mode='remote'
        with self.assertRaises(ia.KitError):self.rt.ensure_model()
    def test_reject_missing_model(self):
        self.cfg['modelo']='outro:tag'
        with self.assertRaises(ia.KitError):self.rt.ensure_model()
    def test_reject_changed_digest(self):
        self.cfg['digest_esperado']='wrong'
        with self.assertRaises(ia.KitError):self.rt.ensure_model()
    def test_no_redirect(self):
        LocalServer.mode='redirect'
        with self.assertRaises(ia.KitError):self.rt.request('/api/version')
    def test_chat_payload_has_limits_no_tools(self):
        msg=[{'role':'user','content':'17+25'}];self.assertEqual(self.rt.chat(msg)[0],'42')
        path,body=LocalServer.received[-1]
        self.assertEqual(path,'/api/chat');self.assertFalse(body['stream']);self.assertEqual(body['options']['num_ctx'],2048);self.assertNotIn('tools',body)
    def test_empty_answer_fails(self):
        LocalServer.mode='empty'
        with self.assertRaises(ia.KitError):self.rt.chat([{'role':'user','content':'oi'}])
    def test_port_busy_no_attach(self):
        with self.assertRaises(ia.KitError):ia.free_port(self.server.server_port)
    def test_external_endpoint_not_exposed(self):
        with self.assertRaises(ia.KitError):self.rt.request('https://example.invalid')
    def test_inherited_cloud_settings_are_removed(self):
        with patch.dict(os.environ,{'OLLAMA_HOST':'https://example.invalid','OLLAMA_DEBUG':'1'}):rt=ia.Runtime(self.cfg)
        self.assertEqual(rt.env['OLLAMA_HOST'],rt.base);self.assertEqual(rt.env['OLLAMA_NO_CLOUD'],'1');self.assertNotIn('OLLAMA_DEBUG',rt.env)
    def test_sensitive_question_limit(self):
        class Args:arquivo=None;texto='x'*12001
        with self.assertRaises(ia.KitError):ia.get_question(Args())
    def test_cloud_tag_rejected_before_start(self):
        cfg=dict(self.cfg,modelo='x:cloud')
        with patch.object(Path,'read_text',return_value=json.dumps(cfg)):
            with self.assertRaises(ia.KitError):ia.profile()
    def test_http_proxy_ignored(self):
        with patch.dict(os.environ,{'HTTP_PROXY':'http://127.0.0.1:1','http_proxy':'http://127.0.0.1:1','NO_PROXY':'','no_proxy':''}):
            rt=ia.Runtime(self.cfg);self.assertEqual(rt.request('/api/version')['version'],'test')
    @unittest.skipUnless(os.name=='posix', 'integraçêo de processo POSIX')
    def test_owned_runtime_starts_answers_and_stops(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fake=root/'ollama'
            fake.write_text('#!'+__import__('sys').executable+'\n'+'''import os,json
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  d={'version':'fake'} if self.path=='/api/version' else {'models':[{'name':'local:tag','size':1234,'digest':'sha256:abc'}]}
  self.send_response(200);self.end_headers();self.wfile.write(json.dumps(d).encode())
 def do_POST(self):
  d=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  out={} if self.path in ('/api/show','/api/generate') else {'message':{'content':'42'},'eval_count':1}
  self.send_response(200);self.end_headers();self.wfile.write(json.dumps(out).encode())
u=urlparse(os.environ['OLLAMA_HOST']);assert os.environ['OLLAMA_NO_CLOUD']=='1'
HTTPServer((u.hostname,u.port),H).serve_forever()
''');fake.chmod(0o755)
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            cfg=dict(self.cfg,porta_runtime=port)
            with patch.object(ia,'ROOT',root),patch.object(ia.shutil,'which',return_value=str(fake)):
                with ia.Runtime(cfg) as rt:
                    proc=rt.process
                    self.assertEqual(rt.ensure_model()['digest'],'sha256:abc')
                    self.assertEqual(rt.chat([{'role':'user','content':'17 + 25'}])[0],'42')
                self.assertIsNotNone(proc.poll())
            with socket.socket() as sock:self.assertNotEqual(sock.connect_ex(('127.0.0.1',port)),0)

if __name__=='__main__':unittest.main()
