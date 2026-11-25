"""Troca só o áudio dos criativos (vídeo copiado sem re-render): gancho e CTA com a voz tratada (voz.py/tratar),
body do pronto cru. Ganho de cada trecho ajustado pra fala (percentil 80) bater com a do body."""
import sys, subprocess, importlib, numpy as np, soundfile as sf
sys.argv = [sys.argv[0]] + sys.argv[1:]
from v3 import Seg, montar_audio
V = "/home/claude/corretores/voz/"
def p80(f, a, b):
    x, sr = sf.read(f); x = x.mean(1) if x.ndim > 1 else x; w = int(sr*.4); s = x[int(a*sr):int(b*sr)]
    r = [20*np.log10(np.sqrt(np.mean(s[i:i+w]**2))+1e-9) for i in range(0, len(s)-w, w//2)]; return np.percentile(r, 80)
def fazer(mod, video, gancho_wav, costura, cta_dur, saida):
    m = importlib.import_module(mod); src_body = m.AUD[1].src; C2 = m.C2
    aud = [Seg(V + gancho_wav, 0.0, costura, fade_out=0.03), Seg(src_body, costura, C2 - costura, fade_in=0.03), Seg(V + "cta10.wav", 0.0, cta_dur)]
    for _ in range(3):   # iguala o nível de fala de gancho e CTA ao body
        montar_audio(aud, [], "/tmp/rx.wav")
        rb = p80("/tmp/rx.wav", costura + 0.5, C2 - 0.3)
        aud[0].ganho += rb - p80("/tmp/rx.wav", 0.2, costura - 0.2); aud[2].ganho += rb - p80("/tmp/rx.wav", C2 + 0.1, C2 + cta_dur - 0.1)
    print(mod, "ganhos", round(aud[0].ganho, 1), round(aud[2].ganho, 1))
    montar_audio(aud, m.SFX, "/tmp/rx_final.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", "/tmp/rx_final.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", saida], check=True)
if __name__ == "__main__":
    O = "/home/claude/corretores/out/"
    fazer("historinha_v4", O + "Corretores - Historinha cliente seguro.mp4", "g4.wav", 15.15, 73.70 - 2050/30, O + "Corretores - Historinha cliente seguro (audio v2).mp4")
    fazer("perguntas_v4", O + "Corretores - Perguntas fora do basico.mp4", "g10.wav", 15.42, 73.70 - 2050/30, O + "Corretores - Perguntas fora do basico (audio v2).mp4")
