# Cantinho Tributário — edição com radar diário

Portal estático de atualização tributária, com dossiês jurídicos iniciais, biblioteca local de estudos e um **radar diário de publicações oficiais**.

## Como publicar no GitHub Pages

1. O repositório público já está criado em [barschyasmin-cmyk/cantinho-tributario](https://github.com/barschyasmin-cmyk/cantinho-tributario). Evite incluir documentos de clientes ou outros dados confidenciais.
2. **Ação indispensável na primeira publicação:** abra [Settings → Pages](https://github.com/barschyasmin-cmyk/cantinho-tributario/settings/pages), encontre **Build and deployment** e selecione **GitHub Actions** em **Source**.
3. Em [Actions](https://github.com/barschyasmin-cmyk/cantinho-tributario/actions), execute o workflow **“Publicar Cantinho Tributário e atualizar radar”** pelo botão **Run workflow**, ou faça um novo commit para iniciar a publicação.
4. Verifique a execução. Quando as etapas **Preparar arquivos do site** e **Publicar site** estiverem concluídas, abra [o Cantinho Tributário](https://barschyasmin-cmyk.github.io/cantinho-tributario/).

**Importante:** o workflow verifica se o GitHub Pages está habilitado. Se estiver desabilitado, a coleta de notícias pode ocorrer normalmente, e o log mostrará uma orientação para ativá-lo. A configuração inicial do Pages requer ação da proprietária da conta.

A rotina em `.github/workflows/atualizacao-diaria.yml` consulta as fontes diariamente às **08h27 (horário de Brasília / UTC-3)** e republica a página após gerar `site/news/updates.json` como parte do artefato publicado. O arquivo gerado durante a execução é publicado no site; não são criados commits diários. O GitHub Actions pode atrasar ou pular execuções, especialmente em períodos de alta demanda. Fluxos agendados de repositórios públicos podem ser desativados por inatividade de 60 dias; acompanhe a aba Actions.

## O que é atualizado automaticamente

- Notícias publicadas nos feeds da **Receita Federal**, **STJ** e **Agência Senado**.
- Título, data de publicação, resumo, órgão e URL de origem; selecionados por palavras-chave tributárias.
- O painel permite distinguir **notícia oficial coletada** de **dossiê jurídico elaborado e conferido**.
- O botão **Conferir novidades** recarrega o arquivo publicado mais recentemente, que é produzido pela rotina diária.

**Limitações:** RSS tem conteúdo, frequência e disponibilidade variáveis. O filtro por palavras-chave pode incluir notícias pouco relevantes ou deixar notícias de fora. A coleta automática não lê necessariamente íntegra dos atos, não confirma teses, não interpreta efeitos jurídicos e não substitui a conferência técnica. Os dossiês jurídicos iniciais usam data de referência **04/11/2026** e exigem revisão editorial posterior para continuar atualizados. Esta implantação não inclui alertas push nem e-mails.

## Testes locais

```bash
python3 -m http.server 8080 --directory site
```

Abra `http://localhost:8080`. O site funciona inicialmente com dossiês incorporados e tenta consultar `site/news/updates.json`. Para testar a rotina de atualização, use `python3 scripts/update_feed.py` numa máquina com internet (nesta entrega, a coleta de fontes ao vivo não pôde ser executada no ambiente de criação).

## Estrutura

- `site/index.html`: portal responsivo, com favoritos, estudos e radar.
- `site/news/updates.json`: publicações obtidas e metadados da coleta.
- `scripts/update_feed.py`: consulta e filtragem de feeds oficiais (biblioteca padrão de Python).
- `.github/workflows/atualizacao-diaria.yml`: execução programada e publicação do GitHub Pages.

**Privacidade:** favoritos, notas e histórico ficam no armazenamento local do navegador usado e não são sincronizados entre dispositivos. Não insira conteúdos sigilosos no repositório público.