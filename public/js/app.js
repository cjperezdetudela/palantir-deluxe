let currentCategory = 'pelis';
let currentPage = 1;
let currentSearch = '';
let currentGenre = '';
let hlsPlayer = null;

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initSearch();
  initGenreFilters();
  updateWatchlistBadge();
  loadCatalog(currentCategory, 1);
  initModals();
  initPlaybackDelegation();

  const storedAdKey = localStorage.getItem('palantir_alldebrid_key');
  if (storedAdKey) {
    saveApiKey(storedAdKey, true);
  }
});

function getWatchlist() {
  try {
    return JSON.parse(localStorage.getItem('palantir_watchlist') || '[]');
  } catch (e) {
    return [];
  }
}

function saveWatchlist(list) {
  localStorage.setItem('palantir_watchlist', JSON.stringify(list));
  updateWatchlistBadge();
}

function updateWatchlistBadge() {
  const list = getWatchlist();
  const badge = document.getElementById('watchlistCountBadge');
  if (badge) {
    if (list.length > 0) {
      badge.textContent = list.length;
      badge.style.display = 'inline-block';
    } else {
      badge.style.display = 'none';
    }
  }
}

function isWatchlisted(tmdb, type) {
  const list = getWatchlist();
  return list.some(item => String(item.tmdb) === String(tmdb) && item.type === type);
}

function toggleWatchlist(item) {
  let list = getWatchlist();
  const existsIdx = list.findIndex(i => String(i.tmdb) === String(item.tmdb) && i.type === item.type);
  if (existsIdx >= 0) {
    list.splice(existsIdx, 1);
  } else {
    list.push({
      tmdb: item.tmdb,
      title: item.title,
      poster: item.poster,
      year: item.year || '',
      rating: item.rating || '',
      type: item.type || 'movie'
    });
  }
  saveWatchlist(list);
  if (currentCategory === 'watchlist') {
    loadCatalog('watchlist', 1);
  }
}

function initNav() {
  const navItems = document.querySelectorAll('.nav-item[data-category]');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const cat = item.dataset.category;
      if (!cat) return;

      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');
      
      currentCategory = cat;
      currentPage = 1;
      
      loadCatalog(cat, 1);
    });
  });
}

function initGenreFilters() {
  const genreChips = document.querySelectorAll('.genre-chip');
  genreChips.forEach(chip => {
    chip.addEventListener('click', () => {
      genreChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentGenre = chip.dataset.genre || '';
      currentPage = 1;
      loadCatalog(currentCategory, 1);
    });
  });
}

function initPlaybackDelegation() {
  document.addEventListener('click', (e) => {
    const bmBtn = e.target.closest('.card-bookmark-btn');
    if (bmBtn) {
      e.stopPropagation();
      e.preventDefault();
      const item = {
        tmdb: bmBtn.dataset.tmdb,
        title: decodeURIComponent(bmBtn.dataset.title || ''),
        poster: bmBtn.dataset.poster,
        year: bmBtn.dataset.year,
        rating: bmBtn.dataset.rating,
        type: bmBtn.dataset.type || 'movie'
      };
      toggleWatchlist(item);
      bmBtn.classList.toggle('active', isWatchlisted(item.tmdb, item.type));
      return;
    }

    const vlcBtn = e.target.closest('.vlc-mini-btn');
    if (vlcBtn) {
      e.stopPropagation();
      e.preventDefault();
      const link = vlcBtn.dataset.link;
      const title = decodeURIComponent(vlcBtn.dataset.title || '');
      playVlcLink(link, title, vlcBtn);
      return;
    }

    const webBtn = e.target.closest('.web-play-btn');
    if (webBtn) {
      e.stopPropagation();
      e.preventDefault();
      const link = webBtn.dataset.link;
      const title = decodeURIComponent(webBtn.dataset.title || '');
      playLink(link, title);
      return;
    }
  });
}

function initAudioFilters() {
  const bar = document.getElementById('audioFilterBar');
  if (!bar) return;
  
  const chips = bar.querySelectorAll('.audio-chip');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      
      const selectedAudio = chip.dataset.audio;
      const linkCards = document.querySelectorAll('.link-btn');
      
      linkCards.forEach(card => {
        const cardAudio = (card.dataset.audio || '').toLowerCase();
        if (selectedAudio === 'all') {
          card.style.display = 'flex';
        } else if (selectedAudio === 'esp') {
          card.style.display = (cardAudio.includes('esp') || cardAudio.includes('spa') || cardAudio.includes('castellano')) ? 'flex' : 'none';
        } else if (selectedAudio === 'lat') {
          card.style.display = cardAudio.includes('lat') ? 'flex' : 'none';
        } else if (selectedAudio === 'eng') {
          card.style.display = (cardAudio.includes('eng') || cardAudio.includes('vo')) ? 'flex' : 'none';
        }
      });
    });
  });
}

function initSearch() {
  const searchInput = document.getElementById('searchInput');
  let searchTimeout = null;
  
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      currentSearch = e.target.value.trim();
      currentPage = 1;
      loadCatalog(currentCategory, 1);
    }, 500);
  });
}

async function loadCatalog(category, page = 1) {
  const grid = document.getElementById('mediaGrid');
  const sectionTitle = document.getElementById('sectionTitle');
  const genreBar = document.getElementById('genreFilterBar');
  grid.innerHTML = '<div class="spinner"></div>';

  if (genreBar) {
    genreBar.style.display = (category === 'pelis' || category === 'series') ? 'flex' : 'none';
  }

  try {
    if (category === 'top10') {
      sectionTitle.textContent = '🔥 TOP 10 Palantir - Lo más popular';
      const resp = await fetch('/api/top10');
      const data = await resp.json();
      renderTop10(data);
      document.getElementById('paginationContainer').innerHTML = '';
      return;
    }

    if (category === 'watchlist') {
      sectionTitle.textContent = currentSearch ? `Búsqueda en Pendientes: "${currentSearch}"` : '🔖 PENDIENTES DE VER (Mi Lista)';
      const list = getWatchlist();
      let filtered = list;
      if (currentSearch) {
        filtered = list.filter(i => (i.title || '').toLowerCase().includes(currentSearch.toLowerCase()));
      }
      renderGrid({ items: filtered }, 'watchlist');
      document.getElementById('paginationContainer').innerHTML = '';
      return;
    }

    let url = '';
    let genreParam = currentGenre ? `&genre=${encodeURIComponent(currentGenre)}` : '';
    let queryParam = currentSearch ? `&query=${encodeURIComponent(currentSearch)}` : '';

    if (category === 'pelis') {
      let label = currentSearch ? `Búsqueda en Películas: "${currentSearch}"` : 'Películas de Palantir';
      if (currentGenre) label += ` [Género: ${currentGenre}]`;
      sectionTitle.textContent = label;
      url = `/api/movies?page=${page}&limit=36${queryParam}${genreParam}`;
    } else if (category === 'series') {
      let label = currentSearch ? `Búsqueda en Series: "${currentSearch}"` : 'Series de TV';
      if (currentGenre) label += ` [Género: ${currentGenre}]`;
      sectionTitle.textContent = label;
      url = `/api/series?page=${page}&limit=36${queryParam}${genreParam}`;
    } else if (category === 'colecciones') {
      sectionTitle.textContent = currentSearch ? `Búsqueda en Colecciones: "${currentSearch}"` : 'Colecciones y Sagas';
      url = `/api/collections?page=${page}&limit=36${queryParam}`;
    } else if (category === 'novedades') {
      sectionTitle.textContent = currentSearch ? `Búsqueda en Novedades: "${currentSearch}"` : '✨ ÚLTIMAS NOVEDADES Y ESTRENOS';
      url = `/api/novedades?page=${page}&limit=36${queryParam}`;
    }

    const resp = await fetch(url);
    const data = await resp.json();
    
    renderGrid(data, category);
    renderPagination(data);
  } catch (err) {
    console.error('Error cargando catálogo:', err);
    grid.innerHTML = '<p style="text-align:center; padding: 3rem; color: #ef4444;">Error al cargar el contenido. Asegúrate de que el servidor backend esté ejecutándose.</p>';
  }
}

function renderTop10(data) {
  const grid = document.getElementById('mediaGrid');
  grid.innerHTML = '';

  const createCard = (item, rankStr) => {
    const card = document.createElement('div');
    card.className = 'card';
    const typeLabel = item.type === 'movie' ? '🎬 Película' : '📺 Serie';

    card.innerHTML = `
      <div class="card-poster-wrap">
        <span class="rank-badge">${rankStr}</span>
        <img src="${item.poster}" alt="${item.title}" loading="lazy" onerror="this.onerror=null; this.src='/api/placeholder?text=${encodeURIComponent(item.title)}&type=poster';">
        <span class="card-badge" style="background: rgba(0,0,0,0.8); font-weight:700;">${typeLabel}</span>
      </div>
      <div class="card-body">
        <h3 class="card-title">${item.title}</h3>
        <div class="card-meta">
          <span>${item.year || ''}</span>
          ${item.rating ? `<span>★ ${item.rating}</span>` : ''}
        </div>
      </div>
    `;

    card.addEventListener('click', () => {
      if (item.type === 'movie') {
        openMovieDetails(item.tmdb);
      } else {
        openSeriesDetails(item.tmdb);
      }
    });

    return card;
  };

  const movieHeading = document.createElement('h3');
  movieHeading.style.gridColumn = '1 / -1';
  movieHeading.style.fontSize = '1.3rem';
  movieHeading.style.margin = '0.5rem 0';
  movieHeading.style.color = '#f59e0b';
  movieHeading.textContent = '🎬 Top 10 Películas más populares';
  grid.appendChild(movieHeading);

  (data.movies || []).forEach(m => {
    let rankBadgeStr = `#${m.rank}`;
    if (m.rank === 1) rankBadgeStr = '🏆 #1';
    else if (m.rank === 2) rankBadgeStr = '🥈 #2';
    else if (m.rank === 3) rankBadgeStr = '🥉 #3';
    grid.appendChild(createCard(m, rankBadgeStr));
  });

  const seriesHeading = document.createElement('h3');
  seriesHeading.style.gridColumn = '1 / -1';
  seriesHeading.style.fontSize = '1.3rem';
  seriesHeading.style.margin = '2rem 0 0.5rem 0';
  seriesHeading.style.color = '#818cf8';
  seriesHeading.textContent = '📺 Top 10 Series más populares';
  grid.appendChild(seriesHeading);

  (data.series || []).forEach(s => {
    let rankBadgeStr = `#${s.rank}`;
    if (s.rank === 1) rankBadgeStr = '🏆 #1';
    else if (s.rank === 2) rankBadgeStr = '🥈 #2';
    else if (s.rank === 3) rankBadgeStr = '🥉 #3';
    grid.appendChild(createCard(s, rankBadgeStr));
  });
}

function renderGrid(data, category) {
  const grid = document.getElementById('mediaGrid');
  grid.innerHTML = '';

  const items = data.items || data;
  if (!items || items.length === 0) {
    grid.innerHTML = '<p style="text-align:center; grid-column: 1/-1; padding: 4rem; color: var(--text-secondary);">No se encontraron resultados.</p>';
    return;
  }

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card';
    
    let typeBadge = '';
    if (category === 'novedades') {
      const typeLabel = item.type === 'movie' ? 'Película' : 'Serie';
      typeBadge = `<span class="card-badge" style="background: linear-gradient(135deg, #ec4899, #8b5cf6); color: #fff; font-weight:700;">✨ Estreno (${typeLabel})</span>`;
    } else if (category === 'pelis' || item.type === 'movie') {
      typeBadge = '<span class="card-badge" style="background: rgba(245, 197, 24, 0.85); color: #000; font-weight:700;">🎬 Película</span>';
    } else if (category === 'series' || item.type === 'series') {
      typeBadge = '<span class="card-badge" style="background: rgba(99, 102, 241, 0.85); color: #fff; font-weight:700;">📺 Serie</span>';
    } else if (category === 'colecciones') {
      typeBadge = '<span class="card-badge" style="background: rgba(16, 185, 129, 0.85); color: #fff; font-weight:700;">📚 Colección</span>';
    }

    const itemType = item.type || (category === 'series' ? 'series' : 'movie');
    const isBookmarked = isWatchlisted(item.tmdb, itemType);

    card.innerHTML = `
      <div class="card-poster-wrap">
        ${category !== 'colecciones' ? `
          <button class="card-bookmark-btn ${isBookmarked ? 'active' : ''}" title="${isBookmarked ? 'Quitar de Pendientes' : 'Guardar en Pendientes'}" data-tmdb="${item.tmdb}" data-type="${itemType}" data-title="${encodeURIComponent(item.title)}" data-poster="${item.poster}" data-year="${item.year || ''}" data-rating="${item.rating || ''}">
            🔖
          </button>
        ` : ''}
        <img src="${item.poster}" alt="${item.title}" loading="lazy" onerror="this.onerror=null; this.src='/api/placeholder?text=${encodeURIComponent(item.title)}&type=poster';">
        ${typeBadge}
      </div>
      <div class="card-body">
        <h3 class="card-title">${item.title}</h3>
        <div class="card-meta">
          <span>${item.year || ''}</span>
          ${item.rating ? `<span>★ ${item.rating}</span>` : ''}
        </div>
      </div>
    `;
    
    card.addEventListener('click', () => {
      if (category === 'pelis' || item.type === 'movie') {
        openMovieDetails(item.tmdb);
      } else if (category === 'series' || item.type === 'series') {
        openSeriesDetails(item.tmdb);
      } else if (category === 'colecciones') {
        currentSearch = item.title;
        document.getElementById('searchInput').value = item.title;
        currentCategory = 'pelis';
        
        document.querySelectorAll('.nav-item[data-category]').forEach(n => {
          n.classList.toggle('active', n.dataset.category === 'pelis');
        });
        
        loadCatalog('pelis', 1);
      }
    });

    grid.appendChild(card);
  });
}

function renderPagination(data) {
  const container = document.getElementById('paginationContainer');
  if (!data.pages || data.pages <= 1) {
    container.innerHTML = '';
    return;
  }

  container.innerHTML = `
    <button class="page-btn" id="prevBtn" ${data.page <= 1 ? 'disabled' : ''}>← Anterior</button>
    <span style="font-weight: 600;">Página ${data.page} de ${data.pages}</span>
    <button class="page-btn" id="nextBtn" ${data.page >= data.pages ? 'disabled' : ''}>Siguiente →</button>
  `;

  document.getElementById('prevBtn')?.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      loadCatalog(currentCategory, currentPage);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  document.getElementById('nextBtn')?.addEventListener('click', () => {
    if (currentPage < data.pages) {
      currentPage++;
      loadCatalog(currentCategory, currentPage);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
}

async function openMovieDetails(tmdbId) {
  const modal = document.getElementById('detailModal');
  modal.classList.add('active');
  
  const content = document.getElementById('modalContent');
  content.innerHTML = '<div class="spinner"></div>';

  try {
    const resp = await fetch(`/api/movie/${tmdbId}`);
    const movie = await resp.json();

    content.innerHTML = `
      <div class="modal-hero" style="background-image: url('${movie.fanart}');">
        <div class="modal-hero-gradient"></div>
      </div>
      <div class="modal-details">
        <div class="modal-header-content">
          <img src="${movie.poster}" class="modal-poster" alt="${movie.title}">
          <div>
            <h2 class="modal-title">${movie.title}</h2>
            <div class="modal-meta-row">
              <span>📅 ${movie.year}</span>
              ${movie.duration ? `<span>⏱️ ${movie.duration} min</span>` : ''}
              ${movie.rating ? `<span>★ ${movie.rating}</span>` : ''}
              <span class="quality-tag">${movie.quality}</span>
            </div>
            <button id="movieWatchlistBtn" style="background: ${isWatchlisted(movie.tmdb, 'movie') ? 'var(--accent-gold)' : 'rgba(255,255,255,0.1)'}; border: 1px solid rgba(255,255,255,0.25); color: ${isWatchlisted(movie.tmdb, 'movie') ? '#000' : '#fff'}; padding: 0.35rem 0.8rem; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.85rem; margin-top: 0.6rem;">
              ${isWatchlisted(movie.tmdb, 'movie') ? '✅ En Pendientes' : '🔖 Guardar en Pendientes'}
            </button>
            <p class="modal-plot">${movie.plot}</p>
          </div>
        </div>

        <div class="links-section">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <h3>Servidores de Reproducción Disponibles</h3>
          </div>
          
          <div class="audio-filter-bar" id="audioFilterBar">
            <span class="audio-filter-title">🎙️ Filtrar Idioma:</span>
            <button class="audio-chip active" data-audio="all">🌐 Todos</button>
            <button class="audio-chip" data-audio="esp">🇪🇸 Castellano</button>
            <button class="audio-chip" data-audio="lat">🇲🇽 Latino</button>
            <button class="audio-chip" data-audio="eng">🇬🇧 VOSE / VO</button>
          </div>

          <div class="links-grid" id="linksGrid">
            ${movie.links && movie.links.length > 0 ? movie.links.map(l => `
              <div class="link-btn" data-audio="${l.audio}">
                <div class="link-info">
                  <div class="link-quality">${l.quality}</div>
                  <div class="link-audio">Audio: ${l.audio} ${l.info ? `(${l.info})` : ''}</div>
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                  <button class="vlc-mini-btn" data-link="${l.link}" data-title="${encodeURIComponent(movie.title)}">🟧 VLC</button>
                  <button class="web-play-btn" data-link="${l.link}" data-title="${encodeURIComponent(movie.title)}">▶ Web</button>
                </div>
              </div>
            `).join('') : '<p style="color: var(--text-secondary);">No hay enlaces directos cargados.</p>'}
          </div>
        </div>
      </div>
    `;
    document.getElementById('movieWatchlistBtn')?.addEventListener('click', () => {
      toggleWatchlist({
        tmdb: movie.tmdb,
        title: movie.title,
        poster: movie.poster,
        year: movie.year,
        rating: movie.rating,
        type: 'movie'
      });
      const btn = document.getElementById('movieWatchlistBtn');
      const inList = isWatchlisted(movie.tmdb, 'movie');
      if (btn) {
        btn.textContent = inList ? '✅ En Pendientes' : '🔖 Guardar en Pendientes';
        btn.style.background = inList ? 'var(--accent-gold)' : 'rgba(255,255,255,0.1)';
        btn.style.color = inList ? '#000' : '#fff';
      }
    });

    initAudioFilters();
  } catch (err) {
    console.error('Error cargando película:', err);
    content.innerHTML = '<p style="padding: 2rem; color:#ef4444;">Error cargando detalles de la película.</p>';
  }
}

async function openSeriesDetails(tmdbId) {
  const modal = document.getElementById('detailModal');
  modal.classList.add('active');
  
  const content = document.getElementById('modalContent');
  content.innerHTML = '<div class="spinner"></div>';

  try {
    const resp = await fetch(`/api/series/${tmdbId}`);
    const show = await resp.json();

    const seasons = show.seasons || {};
    const seasonKeys = Object.keys(seasons).sort((a, b) => a - b);

    content.innerHTML = `
      <div class="modal-hero" style="background-image: url('${show.fanart}');">
        <div class="modal-hero-gradient"></div>
      </div>
      <div class="modal-details">
        <div class="modal-header-content">
          <img src="${show.poster}" class="modal-poster" alt="${show.title}">
          <div>
            <h2 class="modal-title">${show.title}</h2>
            <div class="modal-meta-row">
              <span>📅 ${show.year}</span>
              ${show.rating ? `<span>★ ${show.rating}</span>` : ''}
              <span>${seasonKeys.length} Temporadas</span>
            </div>
            <button id="seriesWatchlistBtn" style="background: ${isWatchlisted(show.tmdb, 'series') ? 'var(--accent-gold)' : 'rgba(255,255,255,0.1)'}; border: 1px solid rgba(255,255,255,0.25); color: ${isWatchlisted(show.tmdb, 'series') ? '#000' : '#fff'}; padding: 0.35rem 0.8rem; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.85rem; margin-top: 0.6rem;">
              ${isWatchlisted(show.tmdb, 'series') ? '✅ En Pendientes' : '🔖 Guardar en Pendientes'}
            </button>
            <p class="modal-plot">${show.plot}</p>
          </div>
        </div>

        <div class="links-section">
          <h3>Episodios y Temporadas</h3>
          
          <div class="audio-filter-bar" id="audioFilterBar">
            <span class="audio-filter-title">🎙️ Filtrar Idioma:</span>
            <button class="audio-chip active" data-audio="all">🌐 Todos</button>
            <button class="audio-chip" data-audio="esp">🇪🇸 Castellano</button>
            <button class="audio-chip" data-audio="lat">🇲🇽 Latino</button>
            <button class="audio-chip" data-audio="eng">🇬🇧 VOSE / VO</button>
          </div>

          <div style="margin-top: 1rem;">
            ${seasonKeys.map(s => `
              <div style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 0.5rem; color: var(--accent-gold);">Temporada ${s}</h4>
                <div class="links-grid">
                  ${seasons[s].map(ep => `
                    <div class="link-btn" data-audio="${ep.audio}">
                      <div class="link-info">
                        <div class="link-quality">Episodio ${ep.episode} (${ep.quality})</div>
                        <div class="link-audio">Audio: ${ep.audio}</div>
                      </div>
                      <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <button class="vlc-mini-btn" data-link="${ep.link}" data-title="${encodeURIComponent(show.title + ' - T' + s + 'E' + ep.episode)}">🟧 VLC</button>
                        <button class="web-play-btn" data-link="${ep.link}" data-title="${encodeURIComponent(show.title + ' - T' + s + 'E' + ep.episode)}">▶ Web</button>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
    document.getElementById('seriesWatchlistBtn')?.addEventListener('click', () => {
      toggleWatchlist({
        tmdb: show.tmdb,
        title: show.title,
        poster: show.poster,
        year: show.year,
        rating: show.rating,
        type: 'series'
      });
      const btn = document.getElementById('seriesWatchlistBtn');
      const inList = isWatchlisted(show.tmdb, 'series');
      if (btn) {
        btn.textContent = inList ? '✅ En Pendientes' : '🔖 Guardar en Pendientes';
        btn.style.background = inList ? 'var(--accent-gold)' : 'rgba(255,255,255,0.1)';
        btn.style.color = inList ? '#000' : '#fff';
      }
    });

    initAudioFilters();
  } catch (err) {
    console.error('Error cargando serie:', err);
    content.innerHTML = '<p style="padding: 2rem; color:#ef4444;">Error cargando detalles de la serie.</p>';
  }
}

let currentStreamUrl = '';

async function playLink(linkStr, title) {
  const playerOverlay = document.getElementById('playerOverlay');
  const playerTitle = document.getElementById('playerTitle');
  const videoPlayer = document.getElementById('videoPlayer');
  
  playerTitle.textContent = `Descodificando enlace de Palantir: ${title}...`;
  playerOverlay.classList.add('active');

  try {
    const resp = await fetch(`/api/resolve?link=${encodeURIComponent(linkStr)}`);
    if (!resp.ok) throw new Error('Falló al descodificar el enlace');
    
    const data = await resp.json();
    const streamUrl = data.stream_url;
    const isUnlocked = data.debrid_unlocked;
    currentStreamUrl = streamUrl;
    
    console.log('Stream desofuscado:', streamUrl);
    playerTitle.textContent = `${title}`;

    const isHoster = streamUrl.includes('1fichier.com') || streamUrl.includes('uptobox.com') || streamUrl.includes('rapidgator.net') || streamUrl.includes('mega.nz');

    if (isHoster && !isUnlocked) {
      closePlayer();
      alert('⚡ REQUERIDO: Este servidor (1fichier) requiere conectar tu cuenta de AllDebrid para reproducir.\n\nHaz clic en el botón "⚡ AllDebrid" en la parte superior para vincular tu cuenta con PIN en 5 segundos.');
      document.getElementById('settingsModal').classList.add('active');
      checkAlldebridStatus();
      return;
    }

    videoPlayer.muted = false;
    videoPlayer.volume = 1.0;

    if (Hls.isSupported() && (streamUrl.includes('.m3u8') || streamUrl.includes('m3u'))) {
      if (hlsPlayer) hlsPlayer.destroy();
      hlsPlayer = new Hls();
      hlsPlayer.loadSource(streamUrl);
      hlsPlayer.attachMedia(videoPlayer);
      hlsPlayer.on(Hls.Events.MANIFEST_PARSED, () => {
        videoPlayer.play().catch(e => {
          console.warn("Autoplay diferido en Chrome:", e);
        });
      });
    } else {
      const isNeedTranscode = streamUrl.toLowerCase().includes('.mkv') || streamUrl.toLowerCase().includes('eac3') || streamUrl.toLowerCase().includes('ac3') || streamUrl.toLowerCase().includes('dts');
      
      if (isNeedTranscode) {
        console.log("Transcodificando audio Dolby EAC3/AC3 a AAC en tiempo real para Chrome...");
        videoPlayer.src = `/api/transcode?url=${encodeURIComponent(streamUrl)}`;
        playerTitle.textContent = `${title} 📻 (Audio adaptado a AAC Stereo)`;
      } else {
        videoPlayer.src = streamUrl;
      }
      
      videoPlayer.load();
      const playPromise = videoPlayer.play();
      if (playPromise !== undefined) {
        playPromise.catch(e => {
          console.warn("Autoplay de Chrome requirió clic del usuario:", e);
          playerTitle.textContent = `${title} (Pulsa ▶ para iniciar)`;
        });
      }
    }
  } catch (err) {
    alert(`No se pudo resolver el vídeo automáticamente: ${err.message}`);
    closePlayer();
  }
}

async function playVlcLink(linkStr, title, btn) {
  if (btn) btn.textContent = '⏳ ...';

  try {
    const resp = await fetch('/api/play/vlc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ link: linkStr })
    });

    const data = await resp.json();
    if (resp.ok && data.status === 'success') {
      const streamUrl = data.stream_url || '';
      const isUnlocked = data.debrid_unlocked;
      const isHoster = streamUrl.includes('1fichier.com') || streamUrl.includes('uptobox.com') || streamUrl.includes('rapidgator.net') || streamUrl.includes('mega.nz');

      if (isHoster && !isUnlocked) {
        alert('⚡ REQUERIDO: Este servidor (1fichier) requiere conectar tu cuenta de AllDebrid para reproducirse en VLC.\n\nPor favor vincula tu cuenta pulsando en ⚡ AllDebrid.');
        document.getElementById('settingsModal').classList.add('active');
        checkAlldebridStatus();
      } else {
        console.log(`VLC iniciado para: ${title}`);
      }
    } else {
      alert(`⚠️ ${data.detail || 'No se pudo iniciar VLC.'}`);
    }
  } catch (err) {
    alert(`Error conectando con VLC: ${err.message}`);
  } finally {
    if (btn) btn.textContent = '🟧 VLC';
  }
}

async function playCurrentInVlc() {
  if (!currentStreamUrl) {
    alert('No hay un vídeo reproduciéndose en este momento.');
    return;
  }
  try {
    const resp = await fetch('/api/play/vlc', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stream_url: currentStreamUrl })
    });
    const data = await resp.json();
    if (resp.ok && data.status === 'success') {
      console.log('VLC iniciado para stream actual');
    } else {
      window.location.href = `vlc://${currentStreamUrl}`;
    }
  } catch (err) {
    window.location.href = `vlc://${currentStreamUrl}`;
  }
}

function initModals() {
  document.getElementById('modalClose')?.addEventListener('click', () => {
    document.getElementById('detailModal').classList.remove('active');
  });
  
  document.getElementById('playerClose')?.addEventListener('click', () => {
    closePlayer();
  });

  document.getElementById('vlcPlayerHeaderBtn')?.addEventListener('click', () => {
    playCurrentInVlc();
  });

  document.getElementById('openInNewTabBtn')?.addEventListener('click', () => {
    if (currentStreamUrl) {
      window.open(currentStreamUrl, '_blank');
    } else {
      alert('No hay un enlace de vídeo activo.');
    }
  });

  document.getElementById('transcodeAudioBtn')?.addEventListener('click', () => {
    if (!currentStreamUrl) {
      alert('No hay un vídeo cargado.');
      return;
    }
    const videoPlayer = document.getElementById('videoPlayer');
    const playerTitle = document.getElementById('playerTitle');
    playerTitle.textContent = `📻 Reparando audio Dolby/EAC3 a stereo AAC en tiempo real...`;
    
    videoPlayer.src = `/api/transcode?url=${encodeURIComponent(currentStreamUrl)}`;
    videoPlayer.load();
    videoPlayer.play().catch(e => {
      console.warn("Transcode play:", e);
    });
  });

  document.getElementById('unmuteAudioBtn')?.addEventListener('click', () => {
    const videoPlayer = document.getElementById('videoPlayer');
    if (videoPlayer) {
      videoPlayer.muted = !videoPlayer.muted;
      videoPlayer.volume = 1.0;
      const btn = document.getElementById('unmuteAudioBtn');
      if (btn) btn.textContent = videoPlayer.muted ? '🔇 Silenciado' : '🔊 Sonido ON';
    }
  });

  initSettingsModal();
}

function closePlayer() {
  const playerOverlay = document.getElementById('playerOverlay');
  const videoPlayer = document.getElementById('videoPlayer');
  
  if (hlsPlayer) {
    hlsPlayer.destroy();
    hlsPlayer = null;
  }
  
  videoPlayer.pause();
  videoPlayer.src = '';
  playerOverlay.classList.remove('active');
}

// AllDebrid Settings Logic
let pinCheckInterval = null;

function initSettingsModal() {
  const settingsBtn = document.getElementById('settingsBtn');
  const settingsModal = document.getElementById('settingsModal');
  const settingsClose = document.getElementById('settingsClose');
  const tabPinBtn = document.getElementById('tabPinBtn');
  const tabKeyBtn = document.getElementById('tabKeyBtn');
  const tabPinSection = document.getElementById('tabPinSection');
  const tabKeySection = document.getElementById('tabKeySection');
  const btnRefreshPin = document.getElementById('btnRefreshPin');
  const btnSaveApiKey = document.getElementById('btnSaveApiKey');
  const btnLogoutAd = document.getElementById('btnLogoutAd');

  settingsBtn?.addEventListener('click', () => {
    settingsModal.classList.add('active');
    checkAlldebridStatus();
  });

  settingsClose?.addEventListener('click', () => {
    settingsModal.classList.remove('active');
    clearInterval(pinCheckInterval);
  });

  tabPinBtn?.addEventListener('click', () => {
    tabPinBtn.classList.add('active');
    tabKeyBtn.classList.remove('active');
    tabPinSection.style.display = 'block';
    tabKeySection.style.display = 'none';
  });

  tabKeyBtn?.addEventListener('click', () => {
    tabKeyBtn.classList.add('active');
    tabPinBtn.classList.remove('active');
    tabKeySection.style.display = 'block';
    tabPinSection.style.display = 'none';
  });

  btnRefreshPin?.addEventListener('click', () => {
    startAlldebridPinFlow();
  });

  btnSaveApiKey?.addEventListener('click', () => {
    const key = document.getElementById('inputApiKey').value.trim();
    if (!key) {
      alert('Por favor ingresa un API Key válido');
      return;
    }
    saveApiKey(key);
  });

  btnLogoutAd?.addEventListener('click', async () => {
    if (confirm('¿Deseas desconectar tu cuenta de AllDebrid?')) {
      localStorage.removeItem('palantir_alldebrid_key');
      await fetch('/api/settings/alldebrid', { method: 'DELETE' });
      document.getElementById('alldebridStatusCard').style.display = 'none';
      document.getElementById('inputApiKey').value = '';
      startAlldebridPinFlow();
    }
  });
}

async function checkAlldebridStatus() {
  try {
    const resp = await fetch('/api/settings/alldebrid');
    const data = await resp.json();

    if (data.has_key) {
      const userOk = await loadAlldebridUserInfo();
      if (!userOk) {
        document.getElementById('alldebridStatusCard').style.display = 'none';
        startAlldebridPinFlow();
      }
    } else {
      document.getElementById('alldebridStatusCard').style.display = 'none';
      startAlldebridPinFlow();
    }
  } catch (err) {
    console.error('Error comprobando estado de AllDebrid:', err);
  }
}

async function loadAlldebridUserInfo() {
  const card = document.getElementById('alldebridStatusCard');
  const usernameEl = document.getElementById('adUsername');
  const statusTextEl = document.getElementById('adStatusText');

  try {
    const resp = await fetch('/api/alldebrid/user');
    if (resp.ok) {
      const data = await resp.json();
      usernameEl.textContent = `👤 ${data.username || 'Usuario AllDebrid'}`;
      
      if (data.premiumUntil) {
        const date = new Date(data.premiumUntil * 1000);
        statusTextEl.textContent = `Suscripción Premium hasta: ${date.toLocaleDateString()}`;
      } else {
        statusTextEl.textContent = 'Cuenta Activa (Prueba/Gratis)';
      }
      card.style.display = 'block';
      return true;
    } else {
      card.style.display = 'none';
      return false;
    }
  } catch (err) {
    console.error('Error al cargar info de usuario AllDebrid:', err);
    card.style.display = 'none';
    return false;
  }
}

async function startAlldebridPinFlow() {
  clearInterval(pinCheckInterval);
  const pinCodeEl = document.getElementById('adPinCode');
  const pinStatusEl = document.getElementById('adPinStatus');
  const userUrlEl = document.getElementById('adUserUrl');

  pinCodeEl.textContent = '....';
  pinStatusEl.textContent = 'Generando nuevo PIN...';
  pinStatusEl.style.color = '#94a3b8';

  try {
    const resp = await fetch('/api/alldebrid/pin/start', { method: 'POST' });
    if (!resp.ok) throw new Error('Falló al obtener el PIN');
    
    const data = await resp.json();
    const pin = data.pin;
    const check = data.check;
    const userUrl = data.user_url || 'https://alldebrid.com/pin';

    pinCodeEl.textContent = pin;
    userUrlEl.href = userUrl;
    userUrlEl.textContent = userUrl;
    pinStatusEl.textContent = 'Esperando a que autorices el PIN en la web de AllDebrid...';

    // Poll status every 3 seconds
    pinCheckInterval = setInterval(async () => {
      try {
        const checkResp = await fetch('/api/alldebrid/pin/check', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pin, check })
        });
        
        const checkData = await checkResp.json();
        if (checkData.status === 'success' && checkData.activated) {
          clearInterval(pinCheckInterval);
          if (checkData.apikey) {
            localStorage.setItem('palantir_alldebrid_key', checkData.apikey);
          }
          pinStatusEl.textContent = '✅ ¡Cuenta de AllDebrid vinculada correctamente!';
          pinStatusEl.style.color = '#10b981';
          loadAlldebridUserInfo();
        } else if (checkData.status === 'error') {
          clearInterval(pinCheckInterval);
          pinStatusEl.textContent = `❌ ${checkData.message || 'PIN caducado'}`;
          pinStatusEl.style.color = '#ef4444';
        }
      } catch (e) {
        console.error('Error polling PIN status:', e);
      }
    }, 3000);

  } catch (err) {
    pinStatusEl.textContent = `Error: ${err.message}`;
    pinStatusEl.style.color = '#ef4444';
  }
}

async function saveApiKey(apiKey, silent = false) {
  try {
    const resp = await fetch('/api/settings/alldebrid', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ enabled: true, apikey: apiKey })
    });
    
    if (resp.ok) {
      localStorage.setItem('palantir_alldebrid_key', apiKey);
      const userOk = await loadAlldebridUserInfo();
      if (!silent) {
        if (userOk) {
          alert('✅ API Key de AllDebrid validada y guardada correctamente');
        } else {
          alert('⚠️ La API Key ingresada no es válida en AllDebrid.');
        }
      }
    } else {
      if (!silent) alert('Error guardando la API Key');
    }
  } catch (err) {
    if (!silent) alert(`Error: ${err.message}`);
  }
}
