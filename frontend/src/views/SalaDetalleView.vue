<template>
  <div class="detalle-sala">
    <div class="home-velo"></div>
    <div class="detalle-wrap">
      <div v-if="cargando" class="estado">Cargando sala...</div>

      <div v-else-if="!sala" class="estado error">
        No se ha podido cargar la sala.
      </div>

      <article v-else class="detalle-card">
        <div class="detalle-main">
          <div class="breadcrumb">ESPACIOS &gt; VALENCIA &gt; {{ sala.location || 'UBICACIÓN' }} &gt; {{ sala.name }}</div>

          <div class="hero-media">
            <img
              :src="sala.image_url || fallbackImage"
              :alt="`Imagen de ${sala.name}`"
              class="detalle-imagen"
              @error="handleImageError"
            />
          </div>

          <div class="copy-card">
            <div class="copy-head">
              <div>
                <p class="badge">{{ sala.is_active ? 'Sala disponible' : 'Sala no disponible' }}</p>
                <h1>{{ sala.name }}</h1>
              </div>

              <button class="favorito-btn" :class="{ activo: esFavorito }" @click="toggleFavorito">
                <span v-if="esFavorito">♥</span>
                <span v-else>♡</span>
                {{ esFavorito ? 'Guardado en favoritos' : 'Añadir a favoritos' }}
              </button>
            </div>

            <p class="descripcion">
              {{ sala.description || 'Esta sala no tiene una descripción todavía.' }}
            </p>

            <div class="info-grid">
              <div class="info-item">
                <span>Capacidad</span>
                <strong>{{ sala.capacity }} personas</strong>
              </div>
              <div class="info-item">
                <span>Precio</span>
                <strong>{{ Number(sala.price_per_hour || 0).toFixed(2) }} €/hora</strong>
              </div>
              <div class="info-item" :class="sala.is_active ? 'ok' : 'warn'">
                <span>Estado</span>
                <strong>{{ sala.is_active ? 'Disponible' : 'No disponible' }}</strong>
              </div>
            </div>

            <section v-if="(sala.equipamiento || []).length" class="equipamiento-section">
              <h2>Equipación</h2>
              <div class="equipamiento-list">
                <span v-for="item in sala.equipamiento" :key="item" class="equipamiento-pill">{{ item }}</span>
              </div>
            </section>

            <div class="acciones">
              <button class="btn-secundario" @click="$router.push('/salas')">Volver al catálogo</button>
              <button class="btn-principal" :disabled="!sala.is_active" @click="irAReservar">
                {{ sala.is_active ? 'Reservar esta sala' : 'Sala no disponible' }}
              </button>
            </div>
          </div>
        </div>

        <aside class="detalle-side">
          <section class="mapa-card">
            <div class="mapa-head">
              <div>
                <p class="mapa-kicker">Ubicación de referencia</p>
                <h2>Mapa</h2>
              </div>
              <span class="mapa-badge">Leaflet</span>
            </div>

            <div ref="mapContainer" class="mapa-leaflet" aria-label="Mapa de la sala"></div>

           
          </section>

          <section class="ubicacion-card">
            <h2>Información del espacio</h2>
            <p class="ubicacion-linea"><strong>Zona:</strong> {{ sala.location || 'Ubicación no definida' }}</p>
            <p class="ubicacion-linea"><strong>Tarifa:</strong> {{ Number(sala.price_per_hour || 0).toFixed(2) }} €/hora</p>
            <p class="ubicacion-linea"><strong>Capacidad:</strong> {{ sala.capacity }} personas</p>
          </section>
        </aside>
      </article>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SalaDetalleView',
  data() {
    return {
      sala: null,
      cargando: true,
      favoritos: [],
      mapInstance: null,
      leafletApi: null,
      leafletReady: false,
      fallbackImage: 'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1400&auto=format&fit=crop'
    };
  },
  async created() {
    this.cargarFavoritos();
    await this.cargarSala();
  },
  async mounted() {
    await this.cargarLeaflet();
    this.renderMap();
  },
  computed: {
    esFavorito() {
      if (!this.sala) return false;
      return this.favoritos.includes(String(this.sala.id));
    },
    coordenadasSala() {
      const coordenadasPorSede = {
        'Sede Ruzafa': [39.4623, -0.3731],
        'Sede El Carmen': [39.4764, -0.3798],
        'Sede Eixample': [39.4675, -0.3692],
        'Sede Cabanyal': [39.4612, -0.3245]
      };

      if (!this.sala) return [39.4699, -0.3763];
      return coordenadasPorSede[this.sala.location] || [39.4699, -0.3763];
    }
  },
  methods: {
    handleImageError(event) {
      const img = event?.target;
      if (!img) return;
      if (img.dataset.fallbackApplied === '1') return;

      img.dataset.fallbackApplied = '1';
      img.src = this.fallbackImage;
    },
    async cargarLeaflet() {
      if (window.L) {
        this.leafletApi = window.L;
        this.leafletReady = true;
        return;
      }

      await this.cargarRecurso('link', {
        rel: 'stylesheet',
        href: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
        integrity: 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=',
        crossorigin: ''
      });

      await this.cargarRecurso('script', {
        src: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
        integrity: 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=',
        crossorigin: ''
      });

      this.leafletApi = window.L;
      this.leafletReady = true;
    },
    cargarRecurso(tagName, atributos) {
      return new Promise((resolve, reject) => {
        const selector = tagName === 'link' ? `link[href="${atributos.href}"]` : `script[src="${atributos.src}"]`;
        const existente = document.querySelector(selector);
        if (existente) {
          resolve();
          return;
        }

        const elemento = document.createElement(tagName);
        Object.entries(atributos).forEach(([key, value]) => {
          if (value !== '') {
            elemento.setAttribute(key, value);
          } else if (key === 'crossorigin') {
            elemento.setAttribute(key, '');
          }
        });

        if (tagName === 'script') {
          elemento.async = true;
          elemento.onload = () => resolve();
          elemento.onerror = reject;
          document.head.appendChild(elemento);
          return;
        }

        document.head.appendChild(elemento);
        resolve();
      });
    },
    cargarFavoritos() {
      try {
        this.favoritos = JSON.parse(localStorage.getItem('favoritos-salas') || '[]');
      } catch (error) {
        this.favoritos = [];
      }
    },
    guardarFavoritos() {
      localStorage.setItem('favoritos-salas', JSON.stringify(this.favoritos));
    },
    async cargarSala() {
      this.cargando = true;
      try {
        const { id } = this.$route.params;
        const response = await axios.get(`http://localhost:8000/api/rooms/${id}`);
        this.sala = response.data;
        this.$nextTick(() => this.renderMap());
      } catch (error) {
        console.error('Error al cargar la sala:', error);
        this.sala = null;
      } finally {
        this.cargando = false;
      }
    },
    toggleFavorito() {
      if (!this.sala) return;

      const salaId = String(this.sala.id);
      if (this.favoritos.includes(salaId)) {
        this.favoritos = this.favoritos.filter(id => id !== salaId);
      } else {
        this.favoritos = [...this.favoritos, salaId];
      }

      this.guardarFavoritos();
    },
    renderMap() {
      if (!this.leafletReady || !this.sala || !this.$refs.mapContainer) return;

      const L = this.leafletApi;
      const coords = this.coordenadasSala;

      if (this.mapInstance) {
        this.mapInstance.remove();
        this.mapInstance = null;
      }

      this.mapInstance = L.map(this.$refs.mapContainer, {
        scrollWheelZoom: false,
        zoomControl: true
      }).setView(coords, 16);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(this.mapInstance);

      L.marker(coords).addTo(this.mapInstance)
        .bindPopup(`<strong>${this.sala.name}</strong><br>${this.sala.location || 'Ubicación de referencia'}`)
        .openPopup();
    },
    irAReservar() {
      if (!this.sala) return;
      this.$router.push({
        path: '/reservas',
        query: { sala: this.sala.id, nombre: this.sala.name }
      });
    }
  },
  watch: {
    '$route.params.id': {
      handler() {
        this.cargarSala();
      },
      immediate: false
    },
    sala() {
      this.$nextTick(() => this.renderMap());
    }
  },
  beforeUnmount() {
    if (this.mapInstance) {
      this.mapInstance.remove();
      this.mapInstance = null;
    }
  }
};
</script>

<style lang="scss" scoped>
.detalle-sala {
  min-height: 100vh;
  padding: 5rem 1.5rem 3rem;
  position: relative;
  z-index: 2;
}

.detalle-sala > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.detalle-wrap {
  max-width: 1080px;
  margin: 0 auto;
}

.estado {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 16px;
  padding: 2rem;
  color: #2b1b17;
  text-align: center;
  text-shadow: none;
}

.estado.error {
  color: #b42318;
}

.detalle-card {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: 1.75rem;
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(43, 27, 23, 0.08);
  text-shadow: none;
}

.detalle-main {
  padding: 1.25rem 1.25rem 1.5rem 1.25rem;
}

.breadcrumb {
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  color: #c7a67d;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.hero-media {
  min-height: 380px;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 1.25rem;
  background: #efe7e0;
}

.detalle-imagen {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.copy-card {
  background: #ffffff;
  border: 1px solid #efdfd4;
  border-radius: 20px;
  padding: 1.4rem;
  box-shadow: 0 10px 24px rgba(43, 27, 23, 0.04);
}

.copy-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.badge {
  display: inline-flex;
  align-self: flex-start;
  margin: 0 0 1rem;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: #f6efe9;
  color: #5a3f37;
  font-size: 0.85rem;
  font-weight: 600;
}

h1 {
  margin: 0;
  color: #2b1b17;
  font-size: 2.5rem;
  line-height: 1.1;
}

.favorito-btn {
  border: 1px solid #e3d6cc;
  background: #fffaf7;
  color: #5a3f37;
  border-radius: 999px;
  padding: 0.8rem 1rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
  transition: transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.favorito-btn.activo {
  background: #fff0f4;
  border-color: #f0c3d2;
  color: #9b2953;
}

.favorito-btn:hover {
  transform: translateY(-1px);
}

.ubicacion {
  margin: 1rem 0 0;
  color: #6f5c55;
  font-weight: 600;
}

.descripcion {
  margin: 1.2rem 0 0;
  color: #6e5e58;
  font-size: 1.02rem;
  line-height: 1.7;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 1.8rem;
}

.info-item {
  background: #fcfaf7;
  border: 1px solid #eadfd8;
  border-radius: 14px;
  padding: 1rem;
}

.info-item span {
  display: block;
  color: #8c7e7a;
  font-size: 0.85rem;
}

.info-item strong {
  display: block;
  margin-top: 0.35rem;
  color: #2b1b17;
  font-size: 1rem;
}

.info-item.ok strong {
  color: #1b7a3d;
}

.info-item.warn strong {
  color: #b42318;
}

.equipamiento-section {
  margin-top: 2rem;
}

.equipamiento-section h2 {
  margin: 0 0 0.9rem;
  color: #2b1b17;
  font-size: 1.2rem;
}

.equipamiento-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.equipamiento-pill {
  background: #f5ede7;
  color: #5a463f;
  border: 1px solid #eadfd8;
  border-radius: 999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
}

.acciones {
  display: flex;
  gap: 0.8rem;
  margin-top: 2.2rem;
}

.detalle-side {
  padding: 1.25rem 1.25rem 1.25rem 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mapa-card,
.ubicacion-card {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 20px;
  box-shadow: 0 10px 24px rgba(43, 27, 23, 0.04);
  padding: 1.1rem;
}

.mapa-head {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 0.9rem;
}

.mapa-kicker {
  margin: 0;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  color: #c7a67d;
  text-transform: uppercase;
}

.mapa-head h2,
.ubicacion-card h2 {
  margin: 0.15rem 0 0;
  color: #2b1b17;
  font-size: 1.15rem;
}

.mapa-badge {
  background: #f6efe9;
  color: #5a3f37;
  border-radius: 999px;
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.mapa-leaflet {
  height: 360px;
  border-radius: 18px;
  overflow: hidden;
}

.mapa-leaflet :deep(.leaflet-container) {
  border-radius: 18px;
}

.mapa-note {
  margin: 0.9rem 0 0;
  color: #6e5e58;
  font-size: 0.92rem;
  line-height: 1.5;
}

.ubicacion-card {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.ubicacion-linea {
  margin: 0;
  color: #5a463f;
  line-height: 1.5;
}

.btn-principal,
.btn-secundario {
  border: none;
  border-radius: 999px;
  padding: 1rem 1.3rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.btn-principal {
  background: #1b4fd6;
  color: #ffffff;
}

.btn-principal:hover:not(:disabled),
.btn-secundario:hover {
  transform: translateY(-1px);
}

.btn-principal:disabled {
  background: #b8c8ef;
  cursor: not-allowed;
}

.btn-secundario {
  background: #f6efe9;
  color: #5a3f37;
}

@media (max-width: 960px) {
  .detalle-card {
    grid-template-columns: 1fr;
  }

  .detalle-main,
  .detalle-side {
    padding: 1rem;
  }

  .copy-head {
    flex-direction: column;
  }

  .hero-media {
    min-height: 260px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .acciones {
    flex-direction: column;
  }

  .mapa-leaflet {
    height: 280px;
  }
}

.home-velo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.25);
  z-index: 1;
  pointer-events: none;
}
</style>