/**
 * Gera a semente fictícia da captura (rodar com cwd=/tmp/app-102):
 *   bun /tmp/telas-102/_gerador/semente.ts
 * - dados.json: linhas de dados_usuario (mesma moto "Minha Titan" da prévia de marketing)
 * - local.json: chaves de localStorage do aparelho (tutorial parado + central de avisos)
 * Usa as funções REAIS do app (textos das notificações, chaves da central e das dicas)
 * e a moto simulada de titan-fixtures.ts (cópia autônoma da prévia com o patch de marketing).
 * (antes: previa-fixtures com o patch de marketing, textos das
 * notificações, chaves da central e das dicas).
 */
import { dadosDoCenario, MOTO_FICTICIA } from "./titan-fixtures.ts";
import { AREAS_DICAS, chaveDicas } from "/tmp/app-102/src/lib/dicas-saude.ts";
import { chaveCentral, type Ocorrencia } from "/tmp/app-102/src/lib/notificacoes/central.ts";
import { textos, cuidadoDe } from "/tmp/app-102/src/lib/notificacoes/textos.ts";
import { carregarFamilia, familiaDoBikeId } from "/tmp/app-102/src/data/perfis-lazy.ts";
import { resolveBike } from "/tmp/app-102/src/data/bikes.ts";

// Relógio fixo da captura (o Playwright instala o mesmo horário na página).
const AGORA = Number(process.env["AGORA_MS"]) || Date.now();
Date.now = () => AGORA;
const UID = process.argv[2] ?? "7f3c2a10-5b1e-4c8d-9a2f-3e6b8d4c1a90";
const OUT = "/tmp/telas-102/_gerador";

function hashTexto(s: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 0x01000193);
  return (h >>> 0).toString(36);
}
const dia = (ms: number) => {
  const d = new Date(ms - 3 * 3600_000);
  return d.toISOString().slice(0, 10);
};

await carregarFamilia(familiaDoBikeId(MOTO_FICTICIA));
const modelo = resolveBike(MOTO_FICTICIA)?.familia.modelo ?? "CG 160";
const bike = MOTO_FICTICIA;
const H = 3_600_000;
const agora = AGORA;

const kVela = `res:${bike}:${dia(agora - 2 * H)}:${hashTexto("vela=Troca vencida")}`;
const kPrev = `prev:${bike}:relacao-lubrificacao:${dia(agora - 20 * H)}`;
const kKm = `km:${bike}:${dia(agora - 50 * H)}`;
const kVal = `res:${bike}:${dia(agora - 74 * H)}:${hashTexto("valvulas=Inspeção próxima")}`;
const oc = (o: Omit<Ocorrencia, "bikeId" | "moto">): Ocorrencia => ({ bikeId: bike, moto: modelo, ...o });
const itens: Ocorrencia[] = [
  oc({ chave: kVela, ...textos.vencido(modelo, cuidadoDe("substituir", "Vela de ignição", "vela"), 0, kVela),
       destino: "item", itemChave: "vela", previsao: false, em: agora - 2 * H, origem: "sistema", lida: false }),
  oc({ chave: kPrev, ...textos.previsao(modelo, cuidadoDe("limpar_lubrificar", "Lubrificar e ajustar a corrente", "relacao-lubrificacao"), kPrev),
       destino: "item", itemChave: "relacao-lubrificacao", previsao: true, em: agora - 20 * H, origem: "sistema", lida: false }),
  oc({ chave: kKm, ...textos.km(modelo, kKm), destino: "km", previsao: false, em: agora - 50 * H, origem: "sistema", lida: true }),
  oc({ chave: kVal, ...textos.proximo(modelo, cuidadoDe("inspecionar", "Folga das válvulas", "valvulas"), 0, kVal),
       destino: "item", itemChave: "valvulas", previsao: false, em: agora - 74 * H, origem: "sistema", lida: true }),
];

const local: Record<string, string> = {};
// "Parar revisão do tutorial" (estado real que o Perfil grava): nenhuma dica por cima das telas.
for (const area of AREAS_DICAS) local[chaveDicas(UID, area)] = JSON.stringify({ v: 1, vistos: {}, parado: true });
local[chaveCentral(UID)] = JSON.stringify({ versao: 1, itens, marcas: {}, conta: hashTexto(`dona|${UID}`) });

const dados = dadosDoCenario("completo") as Record<string, Record<string, unknown>>;
// Média informada pelo dono: ~30 km/dia (mesma moto simulada do marketing); evita o campo zerado em Uso.
dados[`bike:${bike}`] = { ...dados[`bike:${bike}`], mediaKmDiaInformada: 30 };
await Bun.write(`${OUT}/dados.json`, JSON.stringify(dados, null, 1));
await Bun.write(`${OUT}/local.json`, JSON.stringify(local, null, 1));
console.log("modelo:", modelo, "| avisos:", itens.map((i) => i.titulo).join(" / "));
