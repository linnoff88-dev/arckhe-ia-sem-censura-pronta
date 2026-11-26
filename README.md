# IA sem censura pronta

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![IA sem censura pronta](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

[ê°Å¸Å½Â¬ VêÂ­deo: converse com sua IA sem internet (êÂ¡udio em portuguêÂªs).](https://www.youtube.com/watch?v=TJ9omYZdIrE)

Guia completo: https://linnoff88-dev.github.io/

**ValidaêÂ§êÂ£o real em Linux:** execuêÂ§êÂ£o sem rede externa, conversa com contexto e encerramento dos processos prêÂ³prios confirmados. Os 14 testes de software passaram. O modelo acertou os trêÂªs casos testados e respondeu ao tema de debate; isso nêÂ£o mede toda a sua qualidade. Veja [os resultados completos](verificacao/STATUS.md).

## O que êÂ©

Este kit gratuito executa um modelo publicado como abliterated: uma versêÂ£o modificada para ter menos recusas. Serve para quem quer experimentar esse tipo de modelo funcionando, com conversa e leitura de texto. O modelo roda na mêÂ¡quina onde o kit êÂ© instalado, sem API externa de inferêÂªncia. VocêÂª precisa de Python, Ollama e memêÂ³ria suficiente. Menos recusas nêÂ£o garante aceitar todo pedido nem acertar toda resposta.

Este kit pêÂµe um modelo abliterated para conversar com vocêÂª no prêÂ³prio computador: uma versêÂ£o publicada com menos restriêÂ§êÂµes de resposta. O foco êÂ© executar esse modelo de verdade, nêÂ£o apenas explicar o assunto. O padrêÂ£o êÂ© Huihui Qwen3.8-abliterated 27B. Ele tambêÂ©m roda localmente neste kit; menos recusas e privacidade continuam sendo caracterêÂ­sticas diferentes.

**VocêÂª termina conversando com um modelo real.** O kit traz o lanêÂ§ador, o perfil do modelo, a preparaêÂ§êÂ£o dos pesos, conversa com contexto, perguntas por arquivo, um modo Linux sem rede e uma verificaêÂ§êÂ£o executêÂ¡vel. NêÂ£o precisa de chave, assinatura de modelo ou bibliotecas Python extras.

## Requisitos

- Git para clonar, ou [baixe o ZIP](https://github.com/linnoff88-dev/ia-sem-censura-pronta/archive/refs/heads/main.zip) e extraia a pasta.
- Python 3.10 ou superior: [instalador oficial](https://www.python.org/downloads/).
- [Ollama instalado](https://ollama.com/download), no Linux, macOS ou Windows.
- Para o modelo padrêÂ£o: aproximadamente **18 GB de download**, **32 GB de RAM recomendados**, espaêÂ§o livre para os pesos e recursos para o sistema. Contexto padrêÂ£o 2048; o consumo real depende do runtime. GPU êÂ© opcional: CPU funciona, com desempenho diferente.
- No Linux, para o modo sem rede: `bubblewrap` e `iproute2`. O modo exige namespaces de usuêÂ¡rio permitidos pelo sistema.

Verifique antes de comeêÂ§ar:

```bash
python3 --version
ollama --version
```

No Windows, use `py` no lugar de `python3` se necessêÂ¡rio. Depois de instalar o Python ou Ollama, abra um terminal novo. O kit nêÂ£o instala pacotes com privilêÂ©gios nem muda o Ollama usado por outros projetos.

## Instalar e conversar

```bash
git clone https://github.com/linnoff88-dev/ia-sem-censura-pronta.git
cd ia-sem-censura-pronta
python3 ia.py diagnostico
python3 ia.py preparar
python3 ia.py verificar
python3 ia.py conversar
```

`preparar` usa internet para baixar ou conferir os pesos do modelo. Depois, `verificar` e `conversar` usam o modelo local jêÂ¡ baixado, sem baixar automaticamente outro modelo. Os pesos sêÂ£o armazenados pelo prêÂ³prio Ollama, nêÂ£o dentro do repositêÂ³rio.

Na conversa, digite `/limpar` para reiniciar o contexto e `/sair` para encerrar. O kit conserva apenas algumas mensagens recentes em memêÂ³ria e nêÂ£o salva histêÂ³rico. Ao sair, descarrega o modelo e encerra somente sua instêÂ¢ncia e seus processos filhos. O terminal ou o sistema operacional ainda podem registrar o que aparece na tela.

## Linux: conversa com a rede bloqueada para o processo

Depois de preparar os pesos, instale os dois recursos do sistema, se faltarem:

```bash
sudo apt install bubblewrap iproute2
bash sem-rede.sh verificar
bash sem-rede.sh conversar
```

O lanêÂ§ador cria uma rede separada com apenas a interface local `lo`. O modelo e o cliente continuam se comunicando dentro dela; nêÂ£o hêÂ¡ interface para sair êÂ  internet. O computador continua conectado normalmente para os outros programas. Esse modo isola a rede, nêÂ£o os arquivos do usuêÂ¡rio; nêÂ£o êÂ© uma mêÂ¡quina virtual.

Em macOS/Windows, a conversa local funciona pelo `ia.py`; o lanêÂ§ador sem rede êÂ© especêÂ­fico de Linux. Para uma conferêÂªncia manual nesses sistemas, prepare primeiro, desconecte Wi-Fi/cabo e execute `verificar`. NêÂ£o declaramos esse teste realizado em sistemas que nêÂ£o usamos.

## Pergunta êÂºnica e arquivo

```bash
python3 ia.py perguntar "Escreva trêÂªs ideias para organizar uma reuniêÂ£o curta."
python3 ia.py perguntar --arquivo exemplos/primeiro-pedido.txt
```

Para texto sensêÂ­vel, prefira `--arquivo` ou entrada padrêÂ£o: argumentos digitados na linha de comando podem ficar no histêÂ³rico do shell. As respostas sêÂ£o texto; o kit nêÂ£o executa comandos sugeridos pela IA.

## Como saber que funcionou

```bash
python3 ia.py verificar
```

A verificaêÂ§êÂ£o envia uma pergunta real ao modelo (`17 + 25`) e espera `42`. Salva o resultado em `.estado/verificacao.json`, com o digest dos pesos, tokens gerados e interfaces da rede. CêÂ³digo de saêÂ­da 0 significa que esse caso passou; 1 indica resposta diferente; 2 indica erro de preparaêÂ§êÂ£o/execuêÂ§êÂ£o. Uma resposta correta nêÂ£o comprova competêÂªncia geral nem ausêÂªncia de recusas.

Leia tambêÂ©m [verificacao/STATUS.md](verificacao/STATUS.md): ele distingue testes de software de inferêÂªncia realmente executada. O gabarito de um segundo exercêÂ­cio estêÂ¡ em `exemplos/documento-ficticio.txt`.

## O que cada escolha significa

**Privacidade:** quem recebe os dados e onde a tarefa roda. Neste kit, o pedido vai somente êÂ  instêÂ¢ncia prêÂ³pria do Ollama em `127.0.0.1`. Nuvem e ferramentas externas ficam desativadas. O modo Linux sem rede acrescenta uma restriêÂ§êÂ£o do sistema operacional.

**Sem censura:** modelo publicado pelo mantenedor com menos recusas. Este termo nêÂ£o promete aceitar todo pedido, acertar toda resposta ou substituir revisêÂ£o humana. O kit nêÂ£o adiciona filtros de temas e nêÂ£o altera automaticamente o modelo.

## Modelo, versêÂ£o e memêÂ³ria

O perfil usa **`huihui_ai/Qwen3.8-abliterated:27b`**, conferido em 15/11/2026. `perfil.json` registra o digest esperado dos pesos para impedir uma troca silenciosa do modelo. Se o mantenedor mudar a tag e o digest deixar de bater, a execuêÂ§êÂ£o para: confira a nova versêÂ£o antes de atualizar `digest_esperado`. NêÂ£o remova a conferêÂªncia sêÂ³ para passar.

O perfil limita o contexto a 2048 e a resposta a 512 tokens. A conversa tem janela curta; documentos longos precisam ser divididos. O tempo da primeira resposta inclui carregar os pesos. Se houver falta de memêÂ³ria, use uma mêÂ¡quina com capacidade adequada ou escolha conscientemente outro modelo local, ajustando nome e digest. NêÂ£o hêÂ¡ fallback para nuvem.

## Comportamentos importantes

- InstêÂ¢ncia prêÂ³pria, porta exclusiva e nuvem desativada. Porta ocupada gera erro; nunca conectamos silenciosamente a outro serviêÂ§o.
- Proxies herdados nêÂ£o recebem os pedidos e redirecionamentos HTTP sêÂ£o recusados.
- Nome de modelo remoto, pesos ausentes, digest diferente e resposta vazia interrompem a execuêÂ§êÂ£o.
- Nenhum conector, busca na web, agente que executa ferramentas ou publicaêÂ§êÂ£o automêÂ¡tica.
- Privacidade deste fluxo nêÂ£o protege contra malware, administrador do computador, captura de tela, backups ou runtime comprometido.

## Testes de software

```bash
python3 -m unittest discover -s tests -v
```

Esses testes usam um runtime simulado e nêÂ£o contam como teste de modelo. O teste com IA real êÂ© `verificar`.

## DocumentaêÂ§êÂ£o das ferramentas

[Ollama: execuêÂ§êÂ£o local e nuvem](https://docs.ollama.com/faq) êÂ· [API local de conversa](https://docs.ollama.com/api/chat) êÂ· [Modelo padrêÂ£o](https://ollama.com/huihui_ai/Qwen3.8-abliterated:27b).

CêÂ³digo do kit: MIT. Runtime e pesos seguem suas prêÂ³prias licenêÂ§as; os pesos nêÂ£o sêÂ£o redistribuêÂ­dos aqui.

## Se vocêÂª baixou o ZIP

Extraia a pasta. No Windows, abra a pasta que contêÂ©m ia.py, clique na barra de endereêÂ§o, digite powershell e pressione Enter. Execute os comandos Python do guia, usando py se necessêÂ¡rio. Os atalhos preparar.cmd e conversar.cmd tambêÂ©m funcionam com duplo clique. No Linux/macOS, abra Terminal e use cd para entrar na pasta extraêÂ­da; o caminho depende de onde vocêÂª salvou o ZIP. NêÂ£o execute git clone se escolheu ZIP.

Runtime êÂ© o programa que executa o modelo; digest êÂ© a identificaêÂ§êÂ£o exata dos pesos; namespace de rede êÂ© uma rede separada para o processo no Linux. Se houver mudanêÂ§a de digest, o erro mostra os valores esperado e encontrado: confirme a versêÂ£o na pêÂ¡gina oficial da tag antes de decidir atualizar digest_esperado no perfil.json. Sem confirmaêÂ§êÂ£o, mantenha a proteêÂ§êÂ£o.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>