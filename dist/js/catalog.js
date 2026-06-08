document.addEventListener('DOMContentLoaded', () => {
  const revObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add('active'); });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach((el) => revObs.observe(el));

  const grid = document.getElementById('course-grid');
  if (!grid) return;

  const searchInput = document.getElementById('course-search-input');
  const countEl = document.getElementById('course-count');
  const emptyEl = document.getElementById('catalog-empty');
  const sortSelect = document.getElementById('course-sort');
  const pills = document.querySelectorAll('.catalog-pill[data-modality]');
  const areaInputs = document.querySelectorAll('[data-filter-group="area"]');
  const clearBtn = document.getElementById('clear-filters');
  const emptyReset = document.getElementById('empty-reset');
  const cards = [...grid.querySelectorAll('.course-card')];
  const total = cards.length;

  let activeModality = 'all';

  function getAreaFilters() {
    return [...areaInputs].filter((i) => i.checked && !i.disabled).map((i) => i.dataset.filter);
  }

  function countByArea(q, modality) {
    const counts = {};
    cards.forEach((card) => {
      const area = card.dataset.area || '';
      const mod = card.dataset.modalidade || '';
      const text = card.textContent.toLowerCase();
      const matchSearch = !q || text.includes(q);
      const matchMod = modality === 'all' || mod === modality;
      if (matchSearch && matchMod) {
        counts[area] = (counts[area] || 0) + 1;
      }
    });
    return counts;
  }

  function updateAreaFilterUI() {
    const q = (searchInput?.value || '').toLowerCase().trim();
    const counts = countByArea(q, activeModality);

    areaInputs.forEach((input) => {
      const area = input.dataset.filter;
      const count = counts[area] || 0;
      const label = input.closest('.catalog-filter-option');
      const badge = label?.querySelector('[data-count-for]');

      if (badge) badge.textContent = count;

      if (count === 0) {
        input.checked = false;
        input.disabled = true;
        label?.classList.add('is-disabled');
        label?.setAttribute(
          'title',
          'Nenhum curso nesta área para a modalidade ou busca selecionada',
        );
      } else {
        input.disabled = false;
        label?.classList.remove('is-disabled');
        label?.removeAttribute('title');
      }
    });
  }

  function cardMatches(card, q, areas, modality) {
    const text = card.textContent.toLowerCase();
    const mod = card.dataset.modalidade || '';
    const area = card.dataset.area || '';
    const matchSearch = !q || text.includes(q);
    const matchArea = areas.length === 0 || areas.includes(area);
    const matchMod = modality === 'all' || mod === modality;
    return matchSearch && matchArea && matchMod;
  }

  function applyFilters() {
    updateAreaFilterUI();
    const q = (searchInput?.value || '').toLowerCase().trim();
    const areas = getAreaFilters();
    let visible = 0;

    cards.forEach((card) => {
      const show = cardMatches(card, q, areas, activeModality);
      card.classList.toggle('is-hidden', !show);
      if (show) visible++;
    });

    if (countEl) {
      countEl.innerHTML = visible === total
        ? `Mostrando <strong>${total}</strong> cursos`
        : `Mostrando <strong>${visible}</strong> de <strong>${total}</strong> cursos`;
    }
    emptyEl?.classList.toggle('is-visible', visible === 0);
    grid.style.display = visible === 0 ? 'none' : '';
  }

  function sortCards(mode) {
    const sorted = [...cards];
    if (mode === 'az') {
      sorted.sort((a, b) =>
        (a.querySelector('h3')?.textContent || '').localeCompare(b.querySelector('h3')?.textContent || '', 'pt')
      );
    } else if (mode === 'featured') {
      sorted.sort((a, b) => {
        const af = a.classList.contains('course-card--featured') ? 0 : 1;
        const bf = b.classList.contains('course-card--featured') ? 0 : 1;
        return af - bf;
      });
    }
    sorted.forEach((card) => grid.appendChild(card));
  }

  function resetFilters() {
    activeModality = 'all';
    pills.forEach((p) => p.classList.toggle('is-active', p.dataset.modality === 'all'));
    areaInputs.forEach((i) => { i.checked = false; });
    if (searchInput) searchInput.value = '';
    if (sortSelect) sortSelect.value = 'default';
    sortCards('default');
    applyFilters();
  }

  searchInput?.addEventListener('input', applyFilters);
  areaInputs.forEach((i) => i.addEventListener('change', applyFilters));
  clearBtn?.addEventListener('click', resetFilters);
  emptyReset?.addEventListener('click', resetFilters);

  pills.forEach((pill) => {
    pill.addEventListener('click', () => {
      activeModality = pill.dataset.modality;
      pills.forEach((p) => p.classList.toggle('is-active', p === pill));
      applyFilters();
    });
  });

  sortSelect?.addEventListener('change', () => {
    sortCards(sortSelect.value);
    applyFilters();
  });

  const modParam = new URLSearchParams(location.search).get('modalidade');
  if (modParam) {
    const pill = document.querySelector(`.catalog-pill[data-modality="${modParam}"]`);
    if (pill) {
      activeModality = modParam;
      pills.forEach((p) => p.classList.toggle('is-active', p === pill));
    }
  }

  applyFilters();
});
