# IA sem censura pronta

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![IA sem censura pronta](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

[ðŸŽ¬ VÃ­deo: converse com sua IA sem internet (Ã¡udio em portuguÃªs).](https://www.youtube.com/watch?v=TJ9omYZdIrE)

Guia completo: https://linnoff88-dev.github.io/

**ValidaÃ§Ã£o real em Linux:** execuÃ§Ã£o sem rede externa, conversa com contexto e encerramento dos processos prÃ³prios confirmados. Os 14 testes de software passaram. O modelo acertou os trÃªs casos testados e respondeu ao tema de debate; isso nÃ£o mede toda a sua qualidade. Veja [os resultados completos](verificacao/STATUS.md).

## O que Ã©

Este kit gratuito executa um modelo publicado como abliterated: uma versÃ£o modificada para ter menos recusas. Serve para quem quer experimentar esse tipo de modelo funcionando, com conversa e leitura de texto. O modelo roda na mÃ¡quina onde o kit Ã© instalado, sem API externa de inferÃªncia. VocÃª precisa de Python, Ollama e memÃ³ria suficiente. Menos recusas nÃ£o garante aceitar todo pedido nem acertar toda resposta.

Este kit pÃµe um modelo abliterated para conversar com vocÃª no prÃ³prio computador: uma versÃ£o publicada com menos restriÃ§Ãµes de resposta. O foco Ã© executar esse modelo de verdade, nÃ£o apenas explicar o assunto. O padrÃ£o Ã© Huihui Qwen3.8-abliterated 27B. Ele tambÃ©m roda localmente neste kit; menos recusas e privacidade continuam sendo caracterÃ­sticas diferentes.

**VocÃª termina conversando com um modelo real.** O kit traz o lanÃ§ador, o perfil do modelo, a preparaÃ§Ã£o dos pesos, conversa com contexto, perguntas por arquivo, um modo Linux sem rede e uma verificaÃ§Ã£o executÃ¡vel. NÃ£o precisa de chave, assinatura de modelo ou bibliotecas Python extras.

## Requisitos

- Git para clonar, ou [baixe o ZIP](https://github.com/linnoff88-dev/ia-sem-censura-pronta/archive/refs/heads/main.zip) e extraia a pasta.
- Python 3.10 ou superior: [instalador oficial](https://www.python.org/downloads/).
- [Ollama instalado](https://ollama.com/download), no Linux, macOS ou Windows.
- Para o modelo padrÃ£o: aproximadamente **18 GB de download**, **32 GB de RAM recomendados**, espaÃ§o livre para os pesos e recursos para o sistema. Contexto padrÃ£o 2048; o consumo real depende do runtime. GPU Ã© opcional: CPU funciona, com desempenho diferente.
- No Linux, para o modo sem rede: `bubblewrap` e `iproute2`. O modo exige namespaces de usuÃ¡rio permitidos pelo sistema.

Verifique antes de comeÃ§ar:

```bash
python3 --version
ollama --version
```

No Windows, use `py` no lugar de `python3` se necessÃ¡rio. Depois de instalar o Python ou Ollama, abra um terminal novo. O kit nÃ£o instala pacotes com privilÃ©gios nem muda o Ollama usado por outros projetos.

## Instalar e conversar

```bash
git clone https://github.com/linnoff88-dev/ia-sem-censura-pronta.git
cd ia-sem-censura-pronta
python3 ia.py diagnostico
python3 ia.py preparar
python3 ia.py verificar
python3 ia.py conversar
```

`preparar` usa internet para baixar ou conferir os pesos do modelo. Depois, `verificar` e `conversar` usam o modelo local jÃ¡ baixado, sem baixar automaticamente outro modelo. Os pesos sÃ£o armazenados pelo prÃ³prio Ollama, nÃ£o dentro do repositÃ³rio.

Na conversa, digite `/limpar` para reiniciar o contexto e `/sair` para encerrar. O kit conserva apenas algumas mensagens recentes em memÃ³ria e nÃ£o salva histÃ³rico. Ao sair, descarrega o modelo e encerra somente sua instÃ¢ncia e seus processos filhos. O terminal ou o sistema operacional ainda podem registrar o que aparece na tela.

## Linux: conversa com a rede bloqueada para o processo

Depois de preparar os pesos, instale os dois recursos do sistema, se faltarem:

```bash
sudo apt install bubblewrap iproute2
bash sem-rede.sh verificar
bash sem-rede.sh conversar
```

O lanÃ§ador cria uma rede separada com apenas a interface local `lo`. O modelo e o cliente continuam se comunicando dentro dela; nÃ£o hÃ¡ interface para sair Ã  internet. O computador continua conectado normalmente para os outros programas. Esse modo isola a rede, nÃ£o os arquivos do usuÃ¡rio; nÃ£o Ã© uma mÃ¡quina virtual.

Em macOS/Windows, a conversa local funciona pelo `ia.py`; o lanÃ§ador sem rede Ã© especÃ­fico de Linux. Para uma conferÃªncia manual nesses sistemas, prepare primeiro, desconecte Wi-Fi/cabo e execute `verificar`. NÃ£o declaramos esse teste realizado em sistemas que nÃ£o usamos.

## Pergunta Ãºnica e arquivo

```bash
python3 ia.py perguntar "Escreva trÃªs ideias para organizar uma reuniÃ£o curta."
python3 ia.py perguntar --arquivo exemplos/primeiro-pedido.txt
```

Para texto sensÃ­vel, prefira `--arquivo` ou entrada padrÃ£o: argumentos digitados na linha de comando podem ficar no histÃ³rico do shell. As respostas sÃ£o texto; o kit nÃ£o executa comandos sugeridos pela IA.

## Como saber que funcionou

```bash
python3 ia.py verificar
```

A verificaÃ§Ã£o envia uma pergunta real ao modelo (`17 + 25`) e espera `42`. Salva o resultado em `.estado/verificacao.json`, com o digest dos pesos, tokens gerados e interfaces da rede. CÃ³digo de saÃ­da 0 significa que esse caso passou; 1 indica resposta diferente; 2 indica erro de preparaÃ§Ã£o/execuÃ§Ã£o. Uma resposta correta nÃ£o comprova competÃªncia geral nem ausÃªncia de recusas.

Leia tambÃ©m [verificacao/STATUS.md](verificacao/STATUS.md): ele distingue testes de software de inferÃªncia realmente executada. O gabarito de um segundo exercÃ­cio estÃ¡ em `exemplos/documento-ficticio.txt`.

## O que cada escolha significa

**Privacidade:** quem recebe os dados e onde a tarefa roda. Neste kit, o pedido vai somente Ã  instÃ¢ncia prÃ³pria do Ollama em `127.0.0.1`. Nuvem e ferramentas externas ficam desativadas. O modo Linux sem rede acrescenta uma restriÃ§Ã£o do sistema operacional.

**Sem censura:** modelo publicado pelo mantenedor com menos recusas. Este termo nÃ£o promete aceitar todo pedido, acertar toda resposta ou substituir revisÃ£o humana. O kit nÃ£o adiciona filtros de temas e nÃ£o altera automaticamente o modelo.

## Modelo, versÃ£o e memÃ³ria

O perfil usa **`huihui_ai/Qwen3.8-abliterated:27b`**, conferido em 15/11/2026. `perfil.json` registra o digest esperado dos pesos para impedir uma troca silenciosa do modelo. Se o mantenedor mudar a tag e o digest deixar de bater, a execuÃ§Ã£o para: confira a nova versÃ£o antes de atualizar `digest_esperado`. NÃ£o remova a conferÃªncia sÃ³ para passar.

O perfil limita o contexto a 2048 e a resposta a 512 tokens. A conversa tem janela curta; documentos longos precisam ser divididos. O tempo da primeira resposta inclui carregar os pesos. Se houver falta de memÃ³ria, use uma mÃ¡quina com capacidade adequada ou escolha conscientemente outro modelo local, ajustando nome e digest. NÃ£o hÃ¡ fallback para nuvem.

## Comportamentos importantes

- InstÃ¢ncia prÃ³pria, porta exclusiva e nuvem desativada. Porta ocupada gera erro; nunca conectamos silenciosamente a outro serviÃ§o.
- Proxies herdados nÃ£o recebem os pedidos e redirecionamentos HTTP sÃ£o recusados.
- Nome de modelo remoto, pesos ausentes, digest diferente e resposta vazia interrompem a execuÃ§Ã£o.
- Nenhum conector, busca na web, agente que executa ferramentas ou publicaÃ§Ã£o automÃ¡tica.
- Privacidade deste fluxo nÃ£o protege contra malware, administrador do computador, captura de tela, backups ou runtime comprometido.

## Testes de software

```bash
python3 -m unittest discover -s tests -v
```

Esses testes usam um runtime simulado e nÃ£o contam como teste de modelo. O teste com IA real Ã© `verificar`.

## DocumentaÃ§Ã£o das ferramentas

[Ollama: execuÃ§Ã£o local e nuvem](https://docs.ollama.com/faq) Â· [API local de conversa](https://docs.ollama.com/api/chat) Â· [Modelo padrÃ£o](https://ollama.com/huihui_ai/Qwen3.8-abliterated:27b).

CÃ³digo do kit: MIT. Runtime e pesos seguem suas prÃ³prias licenÃ§as; os pesos nÃ£o sÃ£o redistribuÃ­dos aqui.

## Se vocÃª baixou o ZIP

Extraia a pasta. No Windows, abra a pasta que contÃ©m ia.py, clique na barra de endereÃ§o, digite powershell e pressione Enter. Execute os comandos Python do guia, usando py se necessÃ¡rio. Os atalhos preparar.cmd e conversar.cmd tambÃ©m funcionam com duplo clique. No Linux/macOS, abra Terminal e use cd para entrar na pasta extraÃ­da; o caminho depende de onde vocÃª salvou o ZIP. NÃ£o execute git clone se escolheu ZIP.

Runtime Ã© o programa que executa o modelo; digest Ã© a identificaÃ§Ã£o exata dos pesos; namespace de rede Ã© uma rede separada para o processo no Linux. Se houver mudanÃ§a de digest, o erro mostra os valores esperado e encontrado: confirme a versÃ£o na pÃ¡gina oficial da tag antes de decidir atualizar digest_esperado no perfil.json. Sem confirmaÃ§Ã£o, mantenha a proteÃ§Ã£o.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>