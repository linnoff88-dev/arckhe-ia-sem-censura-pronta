# Validação da entrega

- 14 testes de software passaram; incluem processo de servidor de teste e encerramento. Isso é separado da inferência real.
- Testes reais de inferência em Linux: veja `verificacao/prova-real-linux.json` e `verificacao/STATUS.md`. Rede do processo limitada à interface local; processos próprios encerrados e modelos descarregados ao final.
- O teste do documento do modelo leve falhou (600; gabarito 1000); o kit registra a resposta sem alterar o gabarito. O modelo maior acertou esse caso. Não é comparação geral de qualidade nem prova de ausência universal de recusas.
- Guias PT/EN/ES: 18 combinações de projeto, idioma e largura (390, 800 e 1280 px), sem erros JavaScript, links internos ausentes ou transbordamento da página. Imagens carregaram e tema alternou. Comandos preservados entre idiomas.
- Revisão independente final: aprovado, nota 9, sem defeitos obrigatórios.
- GitHub Pages: HTTP 200 nos três idiomas de ambos os projetos.
- Portal: 13 testes, build e TypeScript passaram. Catálogo PRO: 41 testes, 19693 itens, zero IDs removidos; os dois projetos classificados.
- INEMA.INFRA: 12 mensagens de cada tópico e entradas do MENU lidas de volta.
- Vídeo conjunto no lives7: https://www.youtube.com/watch?v=TJ9omYZdIrE; MP4 no Release video-v1.0.0 de ia-privada-pronta. Build strict sem avisos, HyperFrames aprovado e revisão independente nota 8.5. Embed 16:9 nos três idiomas; áudio PT identificado.

Implantação em servidor/nuvem, macOS e Windows não foram testados neste ambiente. O teste de rede isolada é específico do Linux e não isola o sistema de arquivos.
