<template>
  <div class="favoritos-view">
    <div class="home-velo"></div>
    <div class="favoritos-wrap">
      <header class="favoritos-header">
        <h1>Tus salas favoritas</h1>
      </header>

      <div v-if="cargando" class="estado">Cargando favoritos...</div>

      <div v-else-if="!favoritosIds.length" class="estado vacio">
        <h2>Aún no tienes favoritos</h2>
        <p>Entra en el detalle de una sala y pulsa en “Añadir a favoritos”.</p>
        <button class="btn-principal" @click="$router.push('/salas')">Ir al catálogo</button>
      </div>

      <div v-else-if="!salasFavoritas.length" class="estado vacio">
        <h2>No hemos encontrado esas salas</h2>
        <p>Puede que hayan sido eliminadas. Puedes guardar nuevas desde el catálogo.</p>
        <button class="btn-principal" @click="$router.push('/salas')">Ver salas</button>
      </div>

      <section v-else class="grid-favoritos">
        <article
          v-for="sala in salasFavoritas"
          :key="sala.id"
          class="tarjeta-favorito"
          role="button"
          tabindex="0"
          @click="irADetalle(sala.id)"
          @keydown.enter="irADetalle(sala.id)"
          @keydown.space.prevent="irADetalle(sala.id)"
        >
          <img
            :src="sala.image_url || fallbackImage"
            :alt="`Imagen de ${sala.name}`"
            class="sala-imagen"
          />

          <div class="info">
            <h3>{{ sala.name }}</h3>
            <p class="ubicacion">📍 {{ sala.location || 'Ubicación no definida' }}</p>
            <p class="descripcion">{{ sala.description || 'Sin descripción disponible.' }}</p>

            <div class="meta">
              <span>👤 {{ sala.capacity }} personas</span>
              <span class="precio">{{ Number(sala.price_per_hour || 0).toFixed(2) }} €/h</span>
            </div>

            <div v-if="(sala.equipamiento || []).length" class="equipaciones">
              <span v-for="item in sala.equipamiento" :key="`${sala.id}-${item}`" class="pill">{{ item }}</span>
            </div>

            <div class="acciones">
              <button class="btn-secundario" @click.stop="quitarFavorito(sala.id)">Quitar de favoritos</button>
              <button class="btn-principal" :disabled="!sala.is_active" @click.stop="irAReservar(sala)">
                {{ sala.is_active ? 'Reservar' : 'No disponible' }}
              </button>
            </div>
          </div>
        </article>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FavoritosView',
  data() {
    return {
      cargando: true,
      salas: [],
      favoritosIds: [],
      fallbackImage: 'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1400&auto=format&fit=crop'
    };
  },
  computed: {
    salasFavoritas() {
      if (!this.favoritosIds.length) return [];
      const setFavoritos = new Set(this.favoritosIds.map(String));
      return this.salas.filter(sala => setFavoritos.has(String(sala.id)));
    }
  },
  async created() {
    this.cargarFavoritos();
    await this.cargarSalas();
  },
  methods: {
    cargarFavoritos() {
      try {
        const raw = JSON.parse(localStorage.getItem('favoritos-salas') || '[]');
        this.favoritosIds = Array.isArray(raw) ? raw.map(String) : [];
      } catch (error) {
        this.favoritosIds = [];
      }
    },
    guardarFavoritos() {
      localStorage.setItem('favoritos-salas', JSON.stringify(this.favoritosIds));
    },
    async cargarSalas() {
      this.cargando = true;
      try {
        const response = await axios.get('http://localhost:8000/api/rooms/');
        this.salas = response.data || [];
      } catch (error) {
        console.error('Error al cargar salas favoritas:', error);
        this.salas = [];
      } finally {
        this.cargando = false;
      }
    },
    quitarFavorito(salaId) {
      this.favoritosIds = this.favoritosIds.filter(id => id !== String(salaId));
      this.guardarFavoritos();
    },
    irADetalle(salaId) {
      this.$router.push(`/salas/${salaId}`);
    },
    irAReservar(sala) {
      this.$router.push({
        path: '/reservas',
        query: { sala: sala.id, nombre: sala.name }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.favoritos-view {
  min-height: 100vh;
  padding: 2rem 1.5rem 2.5rem;
  position: relative;
  z-index: 2;
}

.favoritos-view > *:not(.home-velo) {
  position: relative;
  z-index: 2;
}

.favoritos-wrap {
  max-width: 1180px;
  margin: 0 auto;
}

.favoritos-header {
  margin-bottom: 3.4rem;
  text-align: center;
}

.favoritos-header h1 {
  color: #ffffff;
  text-shadow: 0 8px 38px rgba(0,0,0,2.95);
  font-family: 'Playfair Display', serif;
  margin: 0;
  font-size: 3.5rem;
  font-weight: 400;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2em;
}

.favoritos-header h1::before,
.favoritos-header h1::after {
  content: '';
  flex: 1 1 60px;
  height: 2px;
  background: linear-gradient(90deg, #fff 60%, #c7a67d 100%);
  opacity: 0.7;
  max-width: 120px;
}


.favoritos-header p {
  margin: 0.45rem 0 0;
  color: #ffffff;
  text-shadow: 0 8px 48px rgba(0,0,0,1.95);
  font-size: 1.5rem;
  font-weight: 500;
}

.estado {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 16px;
  padding: 1.4rem;
  color: #2b1b17;
  text-shadow: none;
}

.estado.vacio {
  text-align: center;
}

.estado.vacio h2 {
  margin: 0;
}

.estado.vacio p {
  margin: 0.5rem 0 1rem;
  color: #6e5e58;
}

.grid-favoritos {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.tarjeta-favorito {
  border: 1px solid #eaddd3;
  border-radius: 16px;
  overflow: hidden;
  background: #ffffff;
  display: grid;
  grid-template-columns: 280px 1fr;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-shadow: none;
}

.tarjeta-favorito:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(43, 27, 23, 0.08);
}

.sala-imagen {
  width: 100%;
  height: 100%;
  min-height: 220px;
  object-fit: cover;
}

.info {
  padding: 1rem 1.2rem;
}

.info h3 {
  margin: 0;
  color: #2b1b17;
}

.ubicacion {
  margin: 0.4rem 0 0;
  color: #5f4f4a;
}

.descripcion {
  margin: 0.6rem 0 0;
  color: #6e5e58;
}

.meta {
  margin-top: 0.8rem;
  display: flex;
  justify-content: space-between;
  color: #5a463f;
  font-weight: 600;
}

.precio {
  color: #1b4fd6;
}

.equipaciones {
  margin-top: 0.8rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.pill {
  background: #f5ede7;
  color: #5a463f;
  border: 1px solid #eadfd8;
  border-radius: 999px;
  font-size: 0.78rem;
  padding: 0.22rem 0.55rem;
}

.acciones {
  margin-top: 1rem;
  display: flex;
  gap: 0.7rem;
}

.btn-principal,
.btn-secundario {
  border: none;
  border-radius: 999px;
  padding: 0.7rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-principal {
  background: #1b4fd6;
  color: #fff;
}

.btn-principal:disabled {
  background: #b8c8ef;
  cursor: not-allowed;
}

.btn-secundario {
  background: #f6efe9;
  color: #5a3f37;
}

@media (max-width: 900px) {
  .tarjeta-favorito {
    grid-template-columns: 1fr;
  }

  .sala-imagen {
    min-height: 190px;
  }

  .acciones {
    flex-direction: column;
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
