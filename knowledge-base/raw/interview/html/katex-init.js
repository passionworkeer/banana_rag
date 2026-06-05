// Shared KaTeX bootstrap for all knowledge pages.
// Loads CSS/JS/auto-render, then auto-renders $$...$$ in <body> on load.
//
// Usage: <script defer src="./katex-init.js"></script>
//   (no other init code needed)

(function () {
  // 1. CSS
  if (!document.querySelector('link[href$="katex.min.css"]')) {
    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = './katex/katex.min.css';
    document.head.appendChild(css);
  }
  // 1b. local overrides (loaded after katex.min.css)
  var ovr = document.createElement('link');
  ovr.rel = 'stylesheet';
  ovr.href = './katex-overrides.css';
  document.head.appendChild(ovr);

  // 2. Main katex JS
  function loadKatex(cb) {
    if (window.katex) return cb();
    var s = document.createElement('script');
    s.src = './katex/katex.min.js';
    s.onload = cb;
    document.head.appendChild(s);
  }

  // 3. auto-render + render
  function render() {
    if (!window.renderMathInElement) {
      var s = document.createElement('script');
      s.src = './katex/auto-render.min.js';
      s.onload = function () {
        window.renderMathInElement(document.body, {
          delimiters: [{left: '$$', right: '$$', display: true}],
          throwOnError: false,
          strict: false,
        });
      };
      document.head.appendChild(s);
    } else {
      window.renderMathInElement(document.body, {
        delimiters: [{left: '$$', right: '$$', display: true}],
        throwOnError: false,
        strict: false,
      });
    }
  }

  loadKatex(render);
})();
