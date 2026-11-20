import base64, subprocess, sys
subprocess.run(['npx','esbuild','main.js','--bundle','--format=iife','--minify','--outfile=bundle.js','--log-level=warning'],check=True)
b=base64.b64encode(open('logo_mask.png','rb').read()).decode()
s=open('shell.html').read().replace('__LOGO_B64__',b).replace('__PARROT_B64__',base64.b64encode(open('assets/Parrot.glb','rb').read()).decode())
js=open('bundle.js').read().replace('</script','<\\/script')
s=s.replace('<script>__BUNDLE__</script>','<script>'+js+'</script>')
open('index.html','w').write(s)
print(len(s))
