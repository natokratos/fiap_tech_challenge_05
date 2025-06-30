Alguns detalhes dos dados:
- Os dados estão em formato JSON.
- Todos os dados sensíveis (de clientes, candidatos e analistas) foram anonimizados utilizando, nomes, nº de celulares, e e-mails aleatórios.
 

Sobre os arquivos:

Jobs.json -> É chaveado pelo código da vaga e possui as informações referentes a vaga aberta no nosso ats divididas em Informações básicas, perfil da vaga e benefícios. Aqui temos dados importantes como, por exemplo:

indicação se é vaga SAP ou não
Cliente solicitante
Nível profissional e nível de idiomas requeridos
Principais atividades e competências técnicas requeridas
 

Prospects.json -> Também é chaveado pelo código da vaga e possui todas as prospecções da vaga.

Lista de prospecções com o código, nome, comentário e situação do candidato na vaga em questão
 

Applicants.json -> É chaveado pelo código do candidato e possui todas as informações referentes ao candidato: Informações básicas, pessoais, profissionais, formação e o cv. Informações importantes desse json:

Nível acadêmico, de inglês e espanhol
Conhecimentos técnicos
Área de atuação
Cv completo
 

Utilização: Por exemplo, a vaga 10976 (chave no Jobs.json), possui 25 prospecções (chave 10976 no prospects.json), onde o candidato “Sr. Thales Freitas”  (chave 41496 no applicants.json) foi contratado.


vagas
id vaga > 
informacoes_basicas > data_requicisao > limite_esperado_para_contratacao > titulo_vaga > vaga_sap > cliente > solicitante_cliente > empresa_divisao > requisitante > analista_responsavel > tipo_contratacao > prazo_contratacao > objetivo_vaga > prioridade_vaga > origem_vaga > superior_imediato, nome, telefone >
perfil_vaga > pais > estado > cidade > bairro > regiao > local_trabalho > vaga_especifica_para_pcd > faixa_etaria > horario_trabalho > nivel profissional > nivel_academico > nivel_ingles > nivel_espanhol > outro_idioma > areas_atuacao > principais_atividades > competencia_tecnicas_e_comportamentais (Consultor PP/QM Sênior com experiencia em projetos de Rollout e implementação SAP ECC, Inglês mandatório, Remoto (Em alguns momentos / fases do projeto deverá estar presente na planta do cliente em Campinas/SP)" > demais_observacoes, Início, Fim, viagens_requeridas, equipamentos_necessarios > beneficios, valor_venda, valor_compra_1, valor_compra_2

prospects
id vaga > titulo > modalidade > prospects > [ nome, codigo, situacao_candidado (Contratado), data_candidatura, ultima_atualizacao, comentario, recrutador ],
 
applicants
id candidato > telefone_recado, telefone, objetivo_profissional, data_criacao, inserido_por, email, local, sabendo_de_nos_por, data_atualizacao, codigo_profissional, nome > informacoes_pessoais, data_aceite, nome, cpf, fonte_indicacao, email, email_secundario, data_nascimento, telefone_celular, telefone_recado, sexo, estado_civil, pcd, endereco, skype, url_linkedin, facebook > informacoes_profissionais, titulo_profissional, area_atuacao, conhecimentos_tecnicos, certificacoes, outras_certificacoes, remuneracao, nivel_profissional > formacao_e_idiomas, nivel_academico, nivel_ingles, nivel_espanhol, outro_idioma > cargo_atual > cv_pt (separada por \n) > cv_en


