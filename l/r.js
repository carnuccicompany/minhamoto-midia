/* Redirecionador MinhaMoto — manda cada pessoa pra loja certa com etiqueta de campanha.
   Sem cookies, sem analytics, sem dado pessoal. Cada página define window.CANAL antes de carregar este arquivo. */
(function () {
  var C = window.CANAL || { ct: 'link', src: 'link', med: 'bio' };
  var APPLE = 'https://apps.apple.com/app/apple-store/id6815447825?pt=129492564&ct=' +
    encodeURIComponent(C.ct) + '&mt=8';
  var REF = 'utm_source=' + C.src + '&utm_medium=' + C.med + '&utm_campaign=organico';
  var PLAY = 'https://play.google.com/store/apps/details?id=com.carnuccicompany.minhamoto&referrer=' +
    encodeURIComponent(REF);

  var a = document.getElementById('btn-apple'), g = document.getElementById('btn-play');
  if (a) a.href = APPLE;
  if (g) g.href = PLAY;

  var ua = navigator.userAgent || '';
  var ios = /iPhone|iPad|iPod/i.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var android = /Android/i.test(ua);
  var destino = ios ? APPLE : (android ? PLAY : null);

  if (destino) {
    document.documentElement.classList.add('indo');
    location.replace(destino);
    setTimeout(function () { document.documentElement.classList.add('demorou'); }, 1800);
  }
})();
