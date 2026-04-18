// ── State ───────────────────────────────────────────────────────────
const STATE = {
  curriculum: null,
  route: null,
};

// ── Subject helpers ──────────────────────────────────────────────────
const SUBJECT_EMOJI = {
  maths: '➗', english: '📖', science: '🔬',
  history: '🏛️', geography: '🌍', computing: '💻',
};
const SUBJECT_LABEL = {
  maths: 'Maths', english: 'English', science: 'Science',
  history: 'History', geography: 'Geography', computing: 'Computing',
};

// ── Router ───────────────────────────────────────────────────────────
function parseRoute(hash) {
  const clean = (hash || '#/').replace(/^#\/?/, '');
  const parts = clean ? clean.split('/') : [];
  if (!parts.length || !parts[0]) return { view: 'home' };
  if (parts[0] === 'year' && parts.length === 2) return { view: 'subjects', year: parts[1] };
  if (parts[0] === 'year' && parts.length === 3) return { view: 'topics',   year: parts[1], subject: parts[2] };
  if (parts[0] === 'year' && parts.length === 4) return { view: 'lesson',   year: parts[1], subject: parts[2], slug: parts[3] };
  if (parts[0] === 'year' && parts.length === 5 && parts[4] === 'play') {
    return { view: 'play', year: parts[1], subject: parts[2], slug: parts[3] };
  }
  return { view: 'home' };
}

async function navigate() {
  STATE.route = parseRoute(location.hash);
  await render();
}

window.addEventListener('hashchange', navigate);
window.addEventListener('DOMContentLoaded', async () => {
  await loadCurriculum();
  navigate();
});

// ── Data ─────────────────────────────────────────────────────────────
async function loadCurriculum() {
  try {
    const res = await fetch('curriculum.json');
    STATE.curriculum = await res.json();
  } catch {
    STATE.curriculum = { years: [] };
  }
}

async function loadLesson(year, subject, slug) {
  try {
    const res = await fetch(`../content/year-${year}/${subject}/${slug}.md`);
    if (!res.ok) return null;
    return res.text();
  } catch {
    return null;
  }
}

function getYear(year) {
  return STATE.curriculum.years.find(y => String(y.year) === String(year)) || null;
}
function getSubject(year, subject) {
  const y = getYear(year);
  return y ? y.subjects.find(s => s.name === subject) : null;
}
function getTopic(year, subject, slug) {
  const s = getSubject(year, subject);
  return s ? s.topics.find(t => t.slug === slug) : null;
}

function getRouteCrumbs(route = STATE.route) {
  const { view, year, subject, slug } = route;
  const crumbs = [{ label: '🏠 Home', href: '#/' }];

  if (year) {
    crumbs.push({ label: `🗓️ Year ${year}`, href: `#/year/${year}` });
  }
  if (subject) {
    const subjectLabel = SUBJECT_LABEL[subject] || subject;
    crumbs.push({ label: `${SUBJECT_EMOJI[subject] || '📚'} ${subjectLabel}`, href: `#/year/${year}/${subject}` });
  }
  if (slug) {
    const topic = getTopic(year, subject, slug);
    crumbs.push({
      label: `📘 ${topic ? topic.title : slug}`,
      href: view === 'play' ? `#/year/${year}/${subject}/${slug}` : null,
    });
  }
  if (view === 'play') {
    crumbs.push({ label: '🎮 Play', href: null });
  }

  return crumbs.map((crumb, index) => ({
    ...crumb,
    current: index === crumbs.length - 1,
  }));
}

function buildRouteNode(item, baseClass) {
  const className = `${baseClass} ${baseClass}--${item.current ? 'current' : 'link'}`;
  const node = item.href && !item.current
    ? el('a', { href: item.href, class: className })
    : el('span', { class: className, 'aria-current': 'page' });
  node.textContent = item.label;
  return node;
}

// ── Breadcrumb ───────────────────────────────────────────────────────
function updateBreadcrumb() {
  const nav = document.getElementById('breadcrumb');
  nav.innerHTML = '';
  const crumbs = getRouteCrumbs();
  crumbs.forEach((c, i) => {
    if (i > 0) {
      const sep = document.createElement('span');
      sep.className = 'breadcrumb__sep';
      sep.textContent = '›';
      nav.appendChild(sep);
    }
    nav.appendChild(buildRouteNode(c, 'breadcrumb__pill'));
  });
}

// ── Render dispatcher ────────────────────────────────────────────────
async function render() {
  const root = document.getElementById('root');

  // Animation view takes over the whole viewport — render outside root
  if (STATE.route.view === 'play') {
    renderPlay(STATE.route.year, STATE.route.subject, STATE.route.slug);
    updateBreadcrumb();
    return;
  }

  // Remove any existing fullscreen animation view
  const existing = document.getElementById('animView');
  if (existing) existing.remove();
  root.style.display = '';

  root.innerHTML = '';
  updateBreadcrumb();
  window.scrollTo({ top: 0, behavior: 'auto' });

  const { view, year, subject, slug } = STATE.route;
  let node;
  if      (view === 'home')     node = renderHome();
  else if (view === 'subjects') node = renderSubjects(year);
  else if (view === 'topics')   node = renderTopics(year, subject);
  else if (view === 'lesson')   node = await renderLesson(year, subject, slug);
  else                          node = renderHome();

  root.appendChild(node);
}

// ── View: Home ───────────────────────────────────────────────────────
function renderHome() {
  const wrap = el('div');
  wrap.appendChild(text('p', 'section-label', '🎓 Primary School Learning'));
  wrap.appendChild(text('h1', 'page-title', 'What are we learning today?'));
  wrap.appendChild(text('p', 'page-sub', 'Pick your year group to get started.'));

  const grid = el('div', { class: 'grid-years' });
  STATE.curriculum.years.forEach((y, i) => {
    const total = y.subjects.reduce((sum, s) => sum + s.topics.length, 0);
    const available = countAvailable(y);

    const card = el('a', { href: `#/year/${y.year}`, class: 'year-card fade-in-up' });
    card.style.animationDelay = `${i * 60}ms`;
    card.appendChild(text('div', 'year-card__number', y.year));
    card.appendChild(text('div', 'year-card__label', `Year ${y.year}`));
    card.appendChild(text('div', 'year-card__age', `Ages ${y.age_range}`));
    const badge = text('div', 'year-card__count', available > 0 ? `${available} / ${total} topics ready` : `${total} topics`);
    card.appendChild(badge);
    grid.appendChild(card);
  });

  wrap.appendChild(grid);
  return wrap;
}

function countAvailable(yearObj) {
  return yearObj.subjects.reduce((s, sub) => s + sub.topics.length, 0);
}

// ── View: Subjects ───────────────────────────────────────────────────
function renderSubjects(year) {
  const y = getYear(year);
  if (!y) return notFound();

  const wrap = el('div');
  wrap.appendChild(backBtn(`#/`, 'All Years'));
  wrap.appendChild(text('p', 'section-label', `Year ${year} · Ages ${y.age_range}`));
  wrap.appendChild(text('h1', 'page-title', `Year ${year} — Choose a subject`));

  const grid = el('div', { class: 'grid-subjects' });
  y.subjects.forEach((s, i) => {
    const card = el('a', {
      href: `#/year/${year}/${s.name}`,
      class: `subject-card fade-in-up`,
      'data-subject': s.name,
    });
    card.style.animationDelay = `${i * 55}ms`;
    card.appendChild(text('div', 'subject-card__emoji', s.emoji));
    card.appendChild(text('div', 'subject-card__name', s.label));
    card.appendChild(text('div', 'subject-card__count', `${s.topics.length} topics`));
    card.appendChild(text('div', 'subject-card__avail', '✓ Content ready'));
    grid.appendChild(card);
  });

  wrap.appendChild(grid);
  return wrap;
}

// ── View: Topics ─────────────────────────────────────────────────────
function renderTopics(year, subject) {
  const s = getSubject(year, subject);
  if (!s) return notFound();

  const wrap = el('div');
  wrap.appendChild(backBtn(`#/year/${year}`, `Year ${year}`));

  const tag = el('div', { class: 'lesson-subject-tag', 'data-subject': subject, style: `--subject-color: var(--${subject})` });
  tag.textContent = `${SUBJECT_EMOJI[subject] || ''} ${s.label}`;
  wrap.appendChild(tag);

  wrap.appendChild(text('h1', 'page-title', `Year ${year} ${s.label}`));
  wrap.appendChild(text('p', 'page-sub', `${s.topics.length} topics · pick one to start learning`));

  const list = el('div', { class: 'topic-list' });
  s.topics.forEach((t, i) => {
    const item = el('a', {
      class: `topic-item fade-in-up available`,
      style: `--subject-color: var(--${subject}); animation-delay: ${i * 40}ms`,
      href: `#/year/${year}/${subject}/${t.slug}`,
    });

    const dot = el('div', { class: 'topic-item__dot' });
    const body = el('div', { class: 'topic-item__body' });
    body.appendChild(text('div', 'topic-item__title', t.title));
    body.appendChild(text('div', 'topic-item__concepts', t.key_concepts.join(' · ')));

    item.appendChild(dot);
    item.appendChild(body);
    item.appendChild(text('span', 'topic-item__arrow', '›'));
    list.appendChild(item);
  });

  wrap.appendChild(list);
  return wrap;
}

// ── View: Lesson ─────────────────────────────────────────────────────
async function renderLesson(year, subject, slug) {
  const topic = getTopic(year, subject, slug);
  const wrap = el('div');
  wrap.appendChild(backBtn(`#/year/${year}/${subject}`, `${SUBJECT_LABEL[subject] || subject}`));

  if (topic) {
    const tag = el('div', { class: 'lesson-subject-tag', style: `--subject-color: var(--${subject})` });
    tag.textContent = `${SUBJECT_EMOJI[subject] || ''} Year ${year} ${SUBJECT_LABEL[subject]}`;
    wrap.appendChild(tag);
  }

  // Skeleton while loading
  const card = el('div', { class: 'lesson-card', style: `--subject-color: var(--${subject})` });
  const skeletonLines = [70, 100, 85, 100, 60, 100, 90].map(w => {
    const s = el('div', { class: 'skeleton', style: `width:${w}%; height:${w < 80 ? '.7rem' : '1rem'}` });
    return s;
  });
  skeletonLines.forEach(s => card.appendChild(s));
  wrap.appendChild(card);

  const md = await loadLesson(year, subject, slug);
  card.innerHTML = '';

  if (!md) {
    card.appendChild(text('p', '', '⚠️ This lesson is not ready yet.'));
  } else {
    const content = el('div', { class: 'lesson-content' });
    renderMarkdown(stripFrontmatter(md), content);
    card.appendChild(content);

    // Play button
    const animPath = `../animations/year-${year}/${subject}/${slug}.html`;
    const playBtn = el('a', {
      href: `#/year/${year}/${subject}/${slug}/play`,
      class: 'play-btn',
      style: `--subject-color: var(--${subject})`,
    });
    playBtn.textContent = '🎮 Play the game!';
    card.appendChild(playBtn);
  }

  return wrap;
}

// ── View: Play ───────────────────────────────────────────────────────
function renderPlay(year, subject, slug) {
  document.getElementById('root').style.display = 'none';

  const existing = document.getElementById('animView');
  if (existing) existing.remove();

  const topic = getTopic(year, subject, slug);
  const animPath = `../animations/year-${year}/${subject}/${slug}.html`;

  const view = el('div', { class: 'anim-view', id: 'animView' });

  const bar = el('div', { class: 'anim-view__bar' });
  const back = el('a', {
    href: `#/year/${year}/${subject}/${slug}`,
    class: 'back-btn',
    style: 'margin-bottom:0',
  });
  back.textContent = 'Back to lesson';
  const title = el('span', { class: 'anim-view__title' });
  title.textContent = topic ? topic.title : slug;

  const trail = el('nav', {
    class: 'anim-view__nav',
    'aria-label': 'Game navigation',
  });
  getRouteCrumbs().forEach(crumb => {
    trail.appendChild(buildRouteNode(crumb, 'anim-view__crumb'));
  });

  bar.appendChild(back);
  bar.appendChild(title);
  bar.appendChild(trail);

  const iframe = el('iframe', {
    src: animPath,
    title: topic ? `${topic.title} interactive game` : 'Learning game',
    loading: 'lazy',
    sandbox: 'allow-scripts',
  });

  view.appendChild(bar);
  view.appendChild(iframe);
  document.body.appendChild(view);
  updateBreadcrumb();
}

// ── Markdown renderer ────────────────────────────────────────────────
function stripFrontmatter(md) {
  const lines = md.split('\n');
  if (lines[0].trim() !== '---') return md;
  const end = lines.indexOf('---', 1);
  if (end === -1) return md;
  return lines.slice(end + 1).join('\n').trimStart();
}

function renderMarkdown(md, container) {
  const lines = md.split('\n');
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Headings
    const hm = line.match(/^(#{1,4})\s+(.+)/);
    if (hm) {
      const tag = `h${hm[1].length}`;
      const h = document.createElement(tag);
      h.textContent = hm[2];
      container.appendChild(h);
      i++; continue;
    }

    // Horizontal rule
    if (/^---+$/.test(line.trim())) {
      container.appendChild(document.createElement('hr'));
      i++; continue;
    }

    // Fenced code block
    if (line.startsWith('```')) {
      const pre = document.createElement('pre');
      const code = document.createElement('code');
      i++;
      const codeLines = [];
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i]);
        i++;
      }
      code.textContent = codeLines.join('\n');
      pre.appendChild(code);
      container.appendChild(pre);
      i++; continue;
    }

    // Details / summary (pass through structure)
    if (line.trim().startsWith('<details>')) {
      const details = document.createElement('details');
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('</details>')) {
        const sm = lines[i].match(/^<summary>(.*?)<\/summary>/);
        if (sm) {
          const summary = document.createElement('summary');
          summary.textContent = sm[1];
          details.appendChild(summary);
        } else if (lines[i].trim()) {
          const p = document.createElement('p');
          applyInline(lines[i].trim(), p);
          details.appendChild(p);
        }
        i++;
      }
      container.appendChild(details);
      i++; continue;
    }

    // Table
    if (line.includes('|') && lines[i + 1] && lines[i + 1].includes('---')) {
      const table = document.createElement('table');
      const thead = document.createElement('thead');
      const tbody = document.createElement('tbody');
      const headerRow = document.createElement('tr');
      parseCells(line).forEach(cell => {
        const th = document.createElement('th');
        th.textContent = cell;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);
      i += 2; // skip header + separator
      while (i < lines.length && lines[i].includes('|')) {
        const tr = document.createElement('tr');
        parseCells(lines[i]).forEach(cell => {
          const td = document.createElement('td');
          applyInline(cell, td);
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
        i++;
      }
      table.appendChild(tbody);
      const tableWrap = document.createElement('div');
      tableWrap.className = 'lesson-table-wrap';
      tableWrap.appendChild(table);
      container.appendChild(tableWrap);
      continue;
    }

    // Unordered list
    if (/^[-*]\s/.test(line)) {
      const ul = document.createElement('ul');
      while (i < lines.length && /^[-*]\s/.test(lines[i])) {
        const li = document.createElement('li');
        const content = lines[i].replace(/^[-*]\s/, '');
        // Checkbox
        if (content.startsWith('[ ] ') || content.startsWith('[x] ')) {
          const cb = el('input', { type: 'checkbox', disabled: '' });
          if (content.startsWith('[x] ')) cb.checked = true;
          li.appendChild(cb);
          const span = document.createElement('span');
          span.textContent = content.slice(4);
          li.appendChild(span);
        } else {
          applyInline(content, li);
        }
        ul.appendChild(li);
        i++;
      }
      container.appendChild(ul);
      continue;
    }

    // Ordered list
    if (/^\d+\.\s/.test(line)) {
      const ol = document.createElement('ol');
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        const li = document.createElement('li');
        applyInline(lines[i].replace(/^\d+\.\s/, ''), li);
        ol.appendChild(li);
        i++;
      }
      container.appendChild(ol);
      continue;
    }

    // Empty line
    if (!line.trim()) { i++; continue; }

    // Paragraph
    const p = document.createElement('p');
    applyInline(line, p);
    container.appendChild(p);
    i++;
  }
}

function parseCells(row) {
  return row.split('|').map(c => c.trim()).filter(c => c.length > 0);
}

function applyInline(text, parent) {
  // Process inline: **bold**, *italic*, `code`
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g);
  parts.forEach(part => {
    if (part.startsWith('**') && part.endsWith('**')) {
      const strong = document.createElement('strong');
      strong.textContent = part.slice(2, -2);
      parent.appendChild(strong);
    } else if (part.startsWith('*') && part.endsWith('*')) {
      const em = document.createElement('em');
      em.textContent = part.slice(1, -1);
      parent.appendChild(em);
    } else if (part.startsWith('`') && part.endsWith('`')) {
      const code = document.createElement('code');
      code.textContent = part.slice(1, -1);
      parent.appendChild(code);
    } else {
      parent.appendChild(document.createTextNode(part));
    }
  });
}

// ── Utilities ────────────────────────────────────────────────────────
function el(tag, attrs = {}) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
  return node;
}

function text(tag, cls, content) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  node.textContent = String(content);
  return node;
}

function backBtn(href, label) {
  const a = el('a', { href, class: 'back-btn' });
  a.textContent = label;
  return a;
}

function notFound() {
  const p = document.createElement('p');
  p.textContent = '⚠️ Page not found.';
  return p;
}
