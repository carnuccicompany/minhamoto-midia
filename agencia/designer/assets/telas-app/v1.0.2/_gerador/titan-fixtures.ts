/**
 * GERADOR DE TELAS (fora do app): cópia autônoma de src/lib/previa-fixtures.ts
 * com o patch de marketing (moto simulada "Minha Titan"). Não é importada pelo
 * app; só o semente.ts usa para montar as linhas do banco falso.
 *
 * Dados fictícios da Prévia visual — fonte única para todas as telas da
 * prévia. Nenhum valor aqui pertence a uma pessoa real: nomes, e-mail, placa,
 * RENAVAM e chassi são obviamente inventados.
 */

export type CenarioPrevia = "completo" | "atencao" | "incompleto" | "varias" | "vazio";

export const CENARIOS: { id: CenarioPrevia; rotulo: string }[] = [
  { id: "completo", rotulo: "Completo" },
  { id: "atencao", rotulo: "Atenção / atrasados" },
  { id: "incompleto", rotulo: "Moto incompleta" },
  { id: "varias", rotulo: "Várias motos" },
  { id: "vazio", rotulo: "Sem motos" },
];

/** Motos públicas do catálogo (modelo, versão e ano), sem dono. */
export const MOTO_FICTICIA = "honda-cg-160__titan__2022";
export const MOTO_FICTICIA_2 = "honda-cb-300f-twister__abs__2024";

export const PERFIL_FICTICIO = {
  nome: "Rafael Souza",
  email: "rafael.souza@email.com",
};

/** Data ISO de n dias atrás (datas relativas: a prévia nunca envelhece). */
export const diasAtras = (n: number) => new Date(Date.now() - n * 86400000).toISOString().slice(0, 10);

/**
 * Moto simulada "Minha Titan" (Honda CG 160 Titan 2022), uso de ~30 km/dia.
 * `o` desloca todas as datas para trás (cenário "atenção": a moto rodou mais
 * 2.000 km sem manutenção, no mesmo ritmo).
 */
function historicoTitan(o: number, atrasado: boolean) {
  const d = (n: number) => diasAtras(n + o);
  const lista = [
    { id: "srv-1", data: d(400), km: 17500, servico: "Troca da vela e do filtro de ar", pecas: "Vela de ignição + filtro de ar", valor: "110,00", obs: "", proxima: "", acao: "trocar" },
    { id: "srv-2", data: d(325), km: 19800, servico: "Troca do kit relação", pecas: "Corrente, coroa e pinhão", valor: "260,00", obs: "", proxima: "", itemChave: "kit-relacao", acao: "trocar" },
    { id: "srv-3", data: d(270), km: 21500, servico: "Troca dos pneus", pecas: "Pneu dianteiro e traseiro", valor: "480,00", obs: "", proxima: "", itemChave: "pneus", acao: "trocar" },
    { id: "srv-3b", data: d(270), km: 21500, servico: "Troca da bateria", pecas: "Bateria 12V 5Ah selada", valor: "260,00", obs: "", proxima: "", itemChave: "bateria", acao: "trocar" },
    atrasado
      ? { id: "srv-4", data: d(190), km: 24000, servico: "Revisão dos 24.000 km", pecas: "Óleo 10W-30, filtro de óleo e folga das válvulas", valor: "190,00", obs: "", proxima: "" }
      : { id: "srv-4", data: d(190), km: 24000, servico: "Revisão dos 24.000 km", pecas: "Checklist do manual e folga das válvulas", valor: "150,00", obs: "", proxima: "", itemChave: "valvulas", acao: "inspecionar" },
    { id: "srv-5", data: d(140), km: 25600, servico: "Pastilhas dianteiras e fluido de freio", pecas: "Pastilhas dianteiras + fluido DOT 4", valor: "150,00", obs: "", proxima: "", acao: "trocar" },
    ...(atrasado
      ? []
      : [{ id: "srv-6", data: d(90), km: 27100, servico: "Troca de óleo e filtro", pecas: "Óleo 10W-30 + filtro", valor: "120,00", obs: "", proxima: "", itemChave: "oleo", acao: "trocar" }]),
    { id: "srv-7", data: d(33), km: 28900, servico: "Lubrificar e ajustar a corrente", pecas: "Lubrificante de corrente", valor: "35,00", obs: "", proxima: "", itemChave: "relacao-lubrificacao", acao: "lubrificar" },
    { id: "srv-8", data: diasAtras(6), km: atrasado ? 31620 : 29620, servico: "Lavagem completa", pecas: "", valor: "45,00", obs: "", proxima: "", acao: "limpar" },
  ];
  return lista;
}

function itensTitan(o: number, atrasado: boolean) {
  const d = (n: number) => diasAtras(n + o);
  return {
    oleo: atrasado
      ? { estado: "feito", ultimoKm: 24000, ultimaData: d(190) }
      : { estado: "feito", ultimoKm: 27100, ultimaData: d(90) },
    "filtro-ar": { estado: "feito", ultimoKm: 17500, ultimaData: d(400) },
    vela: { estado: "feito", ultimoKm: 17500, ultimaData: d(400) },
    valvulas: { estado: "feito", ultimoKm: 24000, ultimaData: d(190) },
    pneus: { estado: "feito", ultimoKm: 21500, ultimaData: d(270) },
    pastilhas: { estado: "feito", ultimoKm: 25600, ultimaData: d(140) },
    "fluido-freio": { estado: "feito", ultimoKm: 25600, ultimaData: d(140) },
    // 1.0.2 (captura): bateria trocada junto com os pneus; sem ela a Saúde fica "Avaliação parcial".
    bateria: { estado: "feito", ultimoKm: 21500, ultimaData: d(270) },
    "relacao-lubrificacao": { estado: "feito", ultimoKm: 28900, ultimaData: d(33) },
    "kit-relacao": { estado: "feito", ultimoKm: 19800, ultimaData: d(325) },
  };
}

const POSTO_A = { postoId: "posto-avenida", posto: "Posto Avenida" };
const POSTO_C = { postoId: "posto-central", posto: "Posto Central" };

const HORAS = ["18:20", "07:45", "12:10", "19:05", "08:30", "17:50", "13:15", "18:40", "07:40"];

function abastecimentosTitan(o: number) {
  const linhas: [number, number, number, number, typeof POSTO_A][] = [
    [73, 27570, 7.6, 5.99, POSTO_C],
    [64, 27860, 7.9, 5.99, POSTO_C],
    [55, 28150, 7.9, 5.99, POSTO_C],
    [46, 28430, 7.6, 5.99, POSTO_C],
    [37, 28700, 7.3, 6.19, POSTO_A],
    [28, 28975, 7.3, 6.19, POSTO_A],
    [19, 29250, 7.2, 6.19, POSTO_A],
    [9, 29530, 7.4, 6.19, POSTO_A],
    [0, 29800, 7.1, 6.19, POSTO_A],
  ];
  return linhas.map(([dias, km, litros, preco, posto], i) => ({
    id: `ab-${i + 1}`,
    quando: `${diasAtras(dias + o)}T${HORAS[i % HORAS.length]}`,
    km,
    litros,
    valor: Math.round(litros * preco * 100) / 100,
    tipo: "Gasolina comum",
    tanque: "cheio",
    ...posto,
  }));
}

function motoTitan(opts: { km: number; o: number; atrasado: boolean }) {
  const d = (n: number) => diasAtras(n + opts.o);
  const leiturasKm = [
    { data: d(400), km: 17500, origem: "manutencao" },
    { data: d(325), km: 19800, origem: "manutencao" },
    { data: d(270), km: 21500, origem: "manutencao" },
    { data: d(190), km: 24000, origem: "manutencao" },
    { data: d(140), km: 25600, origem: "manutencao" },
    { data: d(90), km: 27100, origem: opts.atrasado ? "manual" : "manutencao" },
    { data: d(55), km: 28150, origem: "abastecimento" },
    { data: d(28), km: 28975, origem: "abastecimento" },
    { data: d(9), km: 29530, origem: "abastecimento" },
    { data: d(0), km: 29800, origem: "abastecimento" },
  ];
  if (opts.km > 29800) leiturasKm.push({ data: diasAtras(0), km: opts.km, origem: "manual" });
  return {
    km: opts.km,
    itens: itensTitan(opts.o, opts.atrasado),
    configurado: true,
    ultimaRevisaoKm: opts.atrasado ? 24000 : 27100,
    ultimaRevisaoData: opts.atrasado ? d(190) : d(90),
    observacoes: "",
    apelido: "Minha Titan",
    placa: "BRA2E19",
    fotoPath: "",
    leiturasKm,
    mediaKmDiaInformada: 0,
    frequenciaLembrete: "semanal",
    ultimaVisita: "",
    kmUltimaVisita: 0,
    ultimoResumoVisto: "",
  };
}

/** Segunda moto (cenário "várias motos"): Twister seminova, poucos dados. */
function motoTwister() {
  return {
    km: 6200,
    itens: { oleo: { estado: "feito", ultimoKm: 6000, ultimaData: diasAtras(9) } },
    configurado: true,
    ultimaRevisaoKm: 6000,
    ultimaRevisaoData: diasAtras(9),
    observacoes: "",
    apelido: "Minha Twister",
    placa: "RSO1A23",
    fotoPath: "",
    leiturasKm: [
      { data: diasAtras(40), km: 5100, origem: "manual" },
      { data: diasAtras(9), km: 6000, origem: "manutencao" },
      { data: diasAtras(3), km: 6200, origem: "manual" },
    ],
    mediaKmDiaInformada: 0,
    frequenciaLembrete: "semanal",
    ultimaVisita: "",
    kmUltimaVisita: 0,
    ultimoResumoVisto: "",
  };
}


/**
 * Revisão dos 24.000 km feita na oficina (checklist do manual da CG 160 Titan
 * 2022-2024). A vela não foi trocada nela (tinha sido trocada aos 17.500 km)
 * e, no cenário completo, o óleo foi trocado depois, aos 27.100 km.
 */
const ITENS_MARCO_24000 = [
  "Linha de combustível",
  "Filtro de combustível (unidade)",
  "Acelerador",
  "Tubo de dreno do filtro de ar",
  "Vela de ignição",
  "Folga das válvulas",
  "Óleo do motor",
  "Tela do filtro de óleo",
  "Filtro centrífugo de óleo",
  "Marcha lenta",
  "Sistema de escapamento",
  "Nível do fluido de freio",
  "Pastilhas/sapatas de freio",
  "Sistema de freio",
  "Interruptor da luz de freio",
  "Facho do farol",
  "Embreagem",
  "Cavalete lateral",
  "Suspensões dianteira e traseira",
  "Porcas, parafusos e fixações",
  "Rodas",
  "Alinhamento, rolamentos e cubos das rodas",
  "Folga da coluna de direção",
  "Fluido da suspensão dianteira",
  "Buchas, rolamentos e eixo da suspensão traseira",
  "Articulações do manete e pedal de freio",
  "Conjunto de travas",
  "Guia da corrente de transmissão",
  "Parafusos do suporte do motor e pedal de apoio",
  "Amortecedores e coxins",
  "Eixos das rodas",
  "Alavancas de freio e embreagem",
];

function marcosTitan(o: number, atrasado: boolean) {
  const d = (n: number) => diasAtras(n + o);
  const m: Record<string, { km: number; data: string }> = {};
  for (const item of ITENS_MARCO_24000) {
    m[`24000|${item}`] =
      item === "Vela de ignição"
        ? { km: 17500, data: d(400) }
        : item === "Óleo do motor" && !atrasado
          ? { km: 27100, data: d(90) }
          : { km: 24000, data: d(190) };
  }
  return m;
}

const dadosDocumentais = {
  renavam: "01234567890",
  // Legado sintético: a leitura projeta maiúsculas sem escrever no cenário.
  chassi: "9c2kc2200nr000123",
  cor: "Vermelha",
  proprietario: "Rafael Souza",
  vencimentoLicenciamento: diasAtras(-140),
  seguradora: "Rota Segura Seguros",
  apolice: "RS-2026-004812",
  telefoneSeguro: "(11) 3333-4812",
  contatoEmergencia: "(11) 98765-4321",
  // Campos novos da 1.0.2 (documentos que vencem): tudo em dia.
  validadeCnh: diasAtras(-1290),
  vencimentoSeguro: diasAtras(-190),
  semSeguro: "",
};

export function dadosDoCenario(c: CenarioPrevia = "completo"): Record<string, unknown> {
  const m = MOTO_FICTICIA;
  const atrasado = c === "atencao";
  const o = atrasado ? 66 : 0;
  const base: Record<string, unknown> = {
    [`hist:${m}`]: historicoTitan(o, atrasado),
    [`fuel:${m}`]: abastecimentosTitan(o),
    [`docs:${m}`]: [],
    [`docsinfo:${m}`]: dadosDocumentais,
    [`marcos:${m}`]: marcosTitan(o, atrasado),
  };
  switch (c) {
    case "vazio":
      return { garagem: [] };
    case "incompleto":
      return {
        garagem: [m],
        [`bike:${m}`]: { ...motoTitan({ km: 0, o: 0, atrasado: false }), itens: {}, configurado: false, leiturasKm: [], placa: "", apelido: "" },
      };
    case "atencao":
      return { ...base, garagem: [m], [`bike:${m}`]: motoTitan({ km: 31800, o, atrasado: true }) };
    case "varias":
      return {
        ...base,
        garagem: [m, MOTO_FICTICIA_2],
        [`bike:${m}`]: motoTitan({ km: 29800, o: 0, atrasado: false }),
        [`bike:${MOTO_FICTICIA_2}`]: motoTwister(),
      };
    default:
      return { ...base, garagem: [m], [`bike:${m}`]: motoTitan({ km: 29800, o: 0, atrasado: false }) };
  }
}
