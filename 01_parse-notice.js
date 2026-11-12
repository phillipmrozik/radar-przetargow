// Wyciąganie kluczowych danych z treści ogłoszenia BZP (HTML) / Extracting key facts from a BZP notice (HTML).
// Ta sama logika działa w węźle Code (JavaScript) w workflow n8n.
// The same logic runs in the Code (JavaScript) node of the n8n workflow.

const NL = String.fromCharCode(10);

function toLines(html) {
  const txt = html
    .replace(/<br[^>]*>/gi, NL)
    .replace(/<[/](p|h[0-9]|div|li|tr)>/gi, NL)
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .split(String.fromCharCode(9)).join(' ');
  return txt.split(NL).map((s) => s.split(' ').filter(Boolean).join(' ')).filter(Boolean);
}

function parseNotice(html) {
  const lines = toLines(html);
  const idx = (prefix, from) => {
    for (let i = from || 0; i < lines.length; i++) if (lines[i].indexOf(prefix) === 0) return i;
    return -1;
  };
  const isLabel = (s) => /^[0-9]+[.][0-9]+/.test(s) || s.indexOf('SEKCJA') === 0;

  let description = '';
  const d0 = idx('4.2.2.) Krótki opis');
  if (d0 >= 0) {
    const parts = [];
    for (let i = d0 + 1; i < lines.length && parts.join(' ').length < 900; i++) {
      if (isLabel(lines[i])) break;
      parts.push(lines[i]);
    }
    description = parts.join(' ').slice(0, 900);
  }

  const du = idx('4.2.10.) Okres realizacji');
  const dp = idx('6.4.) Zamawiający wymaga wadium');
  const cd = idx('5.3.) Warunki udziału');
  return {
    description,
    duration: du >= 0 ? lines[du].split(':').slice(1).join(':').trim().slice(0, 120) : '',
    deposit: dp >= 0 ? (lines[dp].indexOf('Tak') >= 0 ? 'yes' : 'no') : '',
    conditions: cd >= 0 ? (lines[cd].indexOf('Tak') >= 0 ? 'yes' : 'no') : '',
  };
}

module.exports = { parseNotice };
