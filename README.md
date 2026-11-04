# Cantinho Tributário — instalação privada

Este repositório contém o portal jurídico e um radar de notícias fiscais alimentado por fontes oficiais. O objetivo é manter **o repositório privado** e publicar **um site com autenticação** para acesso somente às contas autorizadas.

## Passos necessários

1. No GitHub, abra **Settings → General → Danger Zone → Change repository visibility → Make private**. Confirme a alteração no próprio GitHub. Este passo exige permissão administrativa na conta.
2. Conecte a Vercel à conta GitHub e importe o repositório `barschyasmin-cmyk/cantinho-tributario`.
3. Na importação da Vercel, defina **Root Directory = `site`**; escolha **Other** como framework se for necessário. O arquivo `site/index.html` será a entrada.
4. Em **Security → Deployment Protection → Vercel Authentication**, escolha **All Deployments**. Essa opção impede visitantes sem autorização de acessar tanto a produção quanto as prévias. Confirme a proteção em uma aba anônima.
5. Verifique em **Deployments** que o site foi publicado e que você consegue acessá-lo após fazer login na Vercel.

**Não habilite GitHub Pages**: ele pode deixar o site publicamente acessível mesmo quando o repositório é privado.

## Atualizações automáticas

O workflow `.github/workflows/atualizacao-diaria.yml` consulta diariamente feeds da Receita Federal, STJ e Senado, às **8h27 de Brasília (11h27 UTC)**. O script `scripts/update_feed.py` atualiza `site/news/updates.json` e salva as mudanças no repositório privado.

A integração Git da Vercel deverá republicar a versão atualizada a partir desses commits. Após conectar a Vercel, confira se o deploy é acionado pelos commits feitos pelo GitHub Actions; caso contrário, será necessário configurar um deploy hook. GitHub Actions pode atrasar ou deixar de executar tarefas agendadas e consome minutos da cota no repositório privado.

As notícias coletadas automaticamente são marcadas como publicações oficiais; análises jurídicas, impactos e teses exigem confirmação adicional em atos e decisões.

## Arquivos principais

- `site/index.html`: interface do Cantinho Tributário.
- `site/news/updates.json`: notícias coletadas.
- `scripts/update_feed.py`: coletor dos feeds oficiais.
- `.github/workflows/atualizacao-diaria.yml`: rotina diária.

**Privacidade:** favoritos e anotações ficam no armazenamento local do navegador, sem sincronização entre dispositivos. Não inclua documentos de clientes nem segredos nas fontes de notícias ou nos arquivos do projeto.
