<template>
  <div class="home">
    <header class="hero">
      <h1>Catálogo de Salas para Equipos que <em>Avanzan</em></h1>
      <p>Encuentra el espacio ideal según capacidad, ambiente y presupuesto. Reserva en minutos, sin fricción.</p>
    </header>

    <section class="selector-barrios">
      <h2>¿Qué energía encaja hoy con tu equipo?</h2>
      <p>Elige una sede y descubre solo las salas de ese barrio.</p>

      <div class="grid-barrios">
        <article
          v-for="sede in sedesMapeadas"
          :key="sede.location"
          :class="['tarjeta-barrio', { activa: sedeActiva === sede.location }]"
          @click="seleccionarSede(sede.location)"
        >
          <img :src="sede.imagen" :alt="`Ambiente ${sede.barrio}`" class="barrio-imagen" />
          <div class="barrio-overlay">
            <span class="barrio-kicker">{{ sede.kicker }}</span>
            <h3>{{ sede.barrio }}</h3>
            <p>{{ sede.descripcion }}</p>
            <button type="button" class="btn-barrio" @click.stop="seleccionarSede(sede.location)">
              Ver salas
            </button>
          </div>
        </article>
      </div>

      <div v-if="sedeActiva" class="acciones-barrio">
        <button type="button" class="btn-limpiar-sede" @click="limpiarSede">
          Mostrar todas las sedes
        </button>
      </div>
    </section>

    <div v-if="!sedeActiva" class="estado-seleccion-sede">
      Selecciona un barrio para ver sus salas disponibles.
    </div>

    <div v-else ref="catalogoPrincipal" class="contenedor-principal">
      <div class="catalogo-layout">
        <aside class="sidebar-filtros">
          <div class="panel-filtro">
            <div class="sidebar-header sidebar-header-principal">
              <h3>Filtros</h3>
            </div>

            <div class="grupo-filtro">
              <label>Buscar sala</label>
              <input v-model="busquedaNombre" type="text" placeholder="Ej: Sala de Juntas, Podcast..." />
            </div>

            <div class="grupo-filtro">
              <label>Capacidad mínima</label>
              <select v-model.number="capacidadMinima">
                <option value="0">Cualquier capacidad</option>
                <option value="2">Para 2+ personas</option>
                <option value="5">Para 5+ personas</option>
                <option value="10">Para 10+ personas</option>
                <option value="15">Para 15+ personas</option>
                <option value="20">Para 20+ personas</option>
                <option value="30">Para 30+ personas</option>
              </select>
            </div>

            <div class="grupo-filtro grupo-filtro-ubicacion">
              <label>Ubicación</label>
              <select
                v-model="ubicacionSeleccionada"
                :disabled="Boolean(sedeActiva)"
                @change="sincronizarSedeDesdeSelector"
              >
                <option value="">Todas las ubicaciones</option>
                <option v-for="ubicacion in ubicacionesDisponibles" :key="ubicacion" :value="ubicacion">
                  {{ ubicacion }}
                </option>
              </select>
              <p v-if="sedeActiva" class="nota-filtro-bloqueado">
                La sede activa se controla desde las tarjetas superiores.
              </p>
            </div>

            <div class="sidebar-header">
              <h3>Equipación</h3>
              <button
                v-if="equipamientosSeleccionados.length"
                type="button"
                class="limpiar-equipamiento"
                @click="equipamientosSeleccionados = []"
              >
                Limpiar
              </button>
            </div>

            <div class="equipamiento-filtro">
              <label v-for="equipamiento in equipamientosDisponibles" :key="equipamiento" class="equipamiento-opcion">
                <input v-model="equipamientosSeleccionados" type="checkbox" :value="equipamiento" />
                <span>{{ equipamiento }}</span>
              </label>
              <p v-if="!equipamientosDisponibles.length" class="sin-opciones">No hay equipación disponible.</p>
            </div>
          </div>
        </aside>

        <section class="contenido-catalogo">
          <div v-if="cargando" class="spinner">Cargando salas disponibles...</div>
          
          <div v-else-if="salasVisibles.length === 0" class="sin-salas">
            <p>No hay salas disponibles en este momento. Vuelve más tarde.</p>
          </div>

          <div v-else class="grid-salas">
            <article
              v-for="sala in salasVisibles"
              :key="sala.id"
              class="tarjeta-sala"
            >

              <img 
                :src="sala.image_url || defaultRoomImage" 
                alt="Foto de la sala" 
                class="sala-imagen"
                @error="handleRoomImageError"
              />

              <div class="info-sala">
                <h3>{{ sala.name }}</h3>
                <p>{{ sala.description }}</p>
                <p class="ubicacion">📍 {{ sala.location || 'Ubicación no definida' }}</p>
                <div v-if="(sala.equipamiento || []).length" class="equipaciones">
                  <span v-for="item in sala.equipamiento" :key="`${sala.id}-${item}`" class="equipacion-pill">{{ item }}</span>
                </div>
                <div class="detalles">
                  <span>👤 Capacidad: {{ sala.capacity }}</span>
                </div>
                <div class="acciones-sala">
                  <span class="precio">{{ sala.price_per_hour }}€/h</span>
                  <div class="acciones-botones">
                    <button @click.stop="irAReservar(sala)" class="boton-ver">
                      Reservar ahora
                    </button>
                    <button @click="irADetalle(sala)" class="boton-info">
                      Más info
                      <span class="icono-flecha" aria-hidden="true">→</span>
                    </button>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      salas: [],
      sedesMapeadas: [],
      sedeActiva: '',
      busquedaNombre: '',
      capacidadMinima: 0,
      ubicacionSeleccionada: '',
      equipamientosSeleccionados: [],
      defaultRoomImage: 'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=500',
      cargando: true
    }
  },
  async created() {
    // Al cargar la página, pedimos las salas al backend
    try {
      const response = await axios.get('http://localhost:8000/api/rooms/');
      this.salas = response.data;

      const ubicaciones = [...new Set(
        this.salas
          .map(sala => (sala.location || '').trim())
          .filter(Boolean)
      )].sort((a, b) => a.localeCompare(b, 'es'));

      this.sedesMapeadas = ubicaciones.map(location => ({
        location,
        ...this.obtenerMetaSede(location)
      }));
    } catch (error) {
      console.error("Error al traer salas:", error);
    } finally {
      this.cargando = false;
    }
  },
  methods: {
    handleRoomImageError(event) {
      const img = event?.target;
      if (!img) return;
      if (img.dataset.fallbackApplied === '1') return;

      img.dataset.fallbackApplied = '1';
      img.src = this.defaultRoomImage;
    },
    normalizarTexto(texto) {
      return (texto || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim();
    },
    obtenerMetaSede(location) {
      const locationNormalizada = this.normalizarTexto(location);

      const configuraciones = [
        {
          coincide: ['ruzafa', 'russafa'],
          barrio: 'Ruzafa',
          kicker: 'Creatividad urbana',
          descripcion: 'Ambiente dinámico, ideal para equipos de producto y marketing.',
          imagen: 'https://images.unsplash.com/photo-1556761175-b413da4baf72?q=80&w=1200&auto=format&fit=crop'
        },
        {
          coincide: ['carmen'],
          barrio: 'El Carmen',
          kicker: 'Historia + estrategia',
          descripcion: 'Un entorno sereno para reuniones ejecutivas y decisiones clave.',
          imagen: 'https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop'
        },
        {
          coincide: ['eixample', 'ensanche'],
          barrio: 'Eixample',
          kicker: 'Ritmo profesional',
          descripcion: 'Perfecta para sesiones intensivas, workshops y presentaciones.',
          imagen: 'https://images.unsplash.com/photo-1497366811353-6870744d04b2?q=80&w=1200&auto=format&fit=crop'
        },
        {
          coincide: ['cabanyal', 'cabanal', 'cabanal'],
          barrio: 'Cabanyal',
          kicker: 'Inspiración mediterránea',
          descripcion: 'Luz natural y energía relajada para ideación y trabajo profundo.',
          imagen: 'https://images.unsplash.com/photo-1497215842964-222b430dc094?q=80&w=1200&auto=format&fit=crop'
        }
      ];

      const configuracion = configuraciones.find(item =>
        item.coincide.some(alias => locationNormalizada.includes(alias))
      );

      if (configuracion) {
        return {
          barrio: configuracion.barrio,
          kicker: configuracion.kicker,
          descripcion: configuracion.descripcion,
          imagen: configuracion.imagen
        };
      }

      return {
        barrio: location,
        kicker: 'Espacio premium',
        descripcion: 'Descubre las salas disponibles de esta sede con el ambiente ideal para tu equipo.',
        imagen: 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1200&auto=format&fit=crop'
      };
    },
    seleccionarSede(location) {
      this.sedeActiva = location;
      this.ubicacionSeleccionada = location;
      this.busquedaNombre = '';

      this.$nextTick(() => {
        const target = this.$refs.catalogoPrincipal;
        if (!target) return;

        const offset = 20;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    },
    sincronizarSedeDesdeSelector() {
      this.sedeActiva = this.ubicacionSeleccionada || '';
    },
    limpiarSede() {
      this.sedeActiva = '';
      this.ubicacionSeleccionada = '';
      this.busquedaNombre = '';
      this.capacidadMinima = 0;
      this.equipamientosSeleccionados = [];
    },
    irADetalle(sala) {
      this.$router.push(`/salas/${sala.id}`);
    },
    irAReservar(sala) {
      // Pasamos el ID y el nombre por la URL para que ReservasView lo reciba
      this.$router.push({
        path: '/reservas',
        query: { sala: sala.id, nombre: sala.name }
      });
    }
  },
  computed: {
    ubicacionesDisponibles() {
      const ubicaciones = this.salas
        .map(sala => (sala.location || '').trim())
        .filter(Boolean);

      return [...new Set(ubicaciones)].sort((a, b) => a.localeCompare(b, 'es'));
    },
    equipamientosDisponibles() {
      const equipamientos = this.salas.flatMap(sala =>
        Array.isArray(sala.equipamiento)
          ? sala.equipamiento.map(item => (item || '').trim()).filter(Boolean)
          : []
      );

      return [...new Set(equipamientos)].sort((a, b) => a.localeCompare(b, 'es'));
    },
    salasVisibles() {
      // 1. Empezamos filtrando solo las que están activas
      let resultado = this.salas.filter(sala => sala.is_active);

      // 2. Filtramos por nombre si el usuario ha escrito algo
      if (this.busquedaNombre.trim() !== '') {
        const termino = this.busquedaNombre.toLowerCase();
        resultado = resultado.filter(sala => 
          sala.name.toLowerCase().includes(termino)
        );
      }

      // 3. Filtramos por capacidad mínima
      if (this.capacidadMinima > 0) {
        resultado = resultado.filter(sala => sala.capacity >= this.capacidadMinima);
      }

      // 4. Filtramos por ubicación seleccionada
      if (this.ubicacionSeleccionada) {
        resultado = resultado.filter(sala => sala.location === this.ubicacionSeleccionada);
      }

      // 5. Filtramos por equipaciones seleccionadas
      if (this.equipamientosSeleccionados.length) {
        resultado = resultado.filter(sala =>
          Array.isArray(sala.equipamiento) && this.equipamientosSeleccionados.every(item => sala.equipamiento.includes(item))
        );
      }

      return resultado;
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
  height: auto;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  overflow-y: auto;
}

.hero {
  background: transparent;
  color: #fcfaf7;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.75);
  padding: 5.25rem 2rem 2.25rem;
  text-align: center;
  flex-shrink: 0;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 4.5rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero h1 em {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 400;
}

.hero p {
  font-size: 1.2rem;
  color: #f0e8e0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
  max-width: 760px;
  margin: 0 auto;
  line-height: 1.6;
}

.selector-barrios {
  max-width: 1320px;
  margin: 0 auto;
  width: 100%;
  padding: 0 1.25rem 1.5rem;
  color: #f7f2ee;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.55);

  h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    margin-bottom: 0.35rem;
    font-weight: 500;
  }

  > p {
    color: #efe6df;
    margin-bottom: 1rem;
  }
}

.grid-barrios {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.9rem;
}

.tarjeta-barrio {
  position: relative;
  border-radius: 12px;
  min-height: 220px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.28);
  box-shadow: 0 10px 24px rgba(18, 10, 7, 0.22);
  cursor: pointer;
  transition: transform 0.28s ease, box-shadow 0.28s ease;

  &:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 16px 30px rgba(18, 10, 7, 0.3);
  }

  &:hover .barrio-imagen {
    transform: scale(1.08);
  }

  &:hover .btn-barrio,
  &.activa .btn-barrio {
    opacity: 1;
    transform: translateY(0);
  }

  &.activa {
    outline: 2px solid rgba(255, 255, 255, 0.75);
    outline-offset: 2px;
  }
}

.barrio-imagen {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.barrio-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.35rem;
  padding: 1rem;
  background: linear-gradient(180deg, rgba(25, 15, 11, 0.1) 28%, rgba(18, 10, 7, 0.82) 100%);

  h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #fff;
  }

  p {
    margin: 0;
    font-size: 0.88rem;
    line-height: 1.4;
    color: #efe2da;
    min-height: auto;
  }
}

.barrio-kicker {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #f5ddd0;
  font-weight: 600;
}

.btn-barrio {
  margin-top: 0.45rem;
  width: fit-content;
  padding: 0.48rem 0.9rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-size: 0.78rem;
  letter-spacing: 0.02em;
  cursor: pointer;
  backdrop-filter: blur(2px);
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 0.24s ease, transform 0.24s ease, background-color 0.24s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.16);
  }
}

.acciones-barrio {
  margin-top: 0.9rem;
}

.btn-limpiar-sede {
  border: 1px solid rgba(255, 255, 255, 0.75);
  color: #fff;
  background: transparent;
  border-radius: 999px;
  padding: 0.45rem 0.95rem;
  cursor: pointer;
  font-size: 0.84rem;
}

.estado-seleccion-sede {
  max-width: 1320px;
  margin: 0 auto;
  width: calc(100% - 2.5rem);
  background: rgba(255, 255, 255, 0.9);
  color: #2b1b17;
  border: 1px solid #eaddd3;
  border-radius: 12px;
  padding: 1rem 1.15rem;
  text-shadow: none;
}

.contenedor-principal {
  max-width: 1320px;
  margin: 0 auto;
  padding: 2rem 1.25rem;
  width: 100%;
  min-height: auto;
  overflow: visible;
}

.catalogo-layout {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 2rem;
  align-items: start;
  height: auto;
  min-height: auto;
}

.sidebar-filtros {
  height: auto;
}

.panel-filtro {
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(43, 27, 23, 0.04);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: none;
  overflow: visible;
}

.panel-filtro,
.panel-filtro * {
  text-shadow: none !important;
}

.panel-filtro,
.contenido-catalogo {
  scrollbar-width: thin;
  scrollbar-color: #bda79b #f6efe9;
}

.panel-filtro::-webkit-scrollbar,
.contenido-catalogo::-webkit-scrollbar {
  width: 10px;
}

.panel-filtro::-webkit-scrollbar-track,
.contenido-catalogo::-webkit-scrollbar-track {
  background: #f6efe9;
  border-radius: 999px;
}

.panel-filtro::-webkit-scrollbar-thumb,
.contenido-catalogo::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #c8b1a3, #a78779);
  border-radius: 999px;
  border: 2px solid #f6efe9;
}

.panel-filtro::-webkit-scrollbar-thumb:hover,
.contenido-catalogo::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #b7998c, #967467);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.85rem;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #2b1b17;
}

.sidebar-header-principal {
  margin-bottom: 0;
}

.contenido-catalogo {
  min-width: 0;
  min-height: auto;
  height: auto;
  overflow: visible;
  padding-right: 0.35rem;
  --salas-gap: 1.2rem;
  --salas-buffer: 0.9rem;
}

.grid-salas {
  display: grid;
  grid-template-columns: 1fr;
  grid-auto-rows: auto;
  gap: var(--salas-gap);
  min-height: auto;
  padding-bottom: var(--salas-buffer);
  box-sizing: border-box;
}

.tarjeta-sala {
  display: grid;
  grid-template-columns: 300px 1fr;
  min-height: 220px;
  height: auto;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #eaddd3;
  box-shadow: 0 10px 22px rgba(43, 27, 23, 0.04);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  text-shadow: none;
  cursor: default;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(43, 27, 23, 0.07);
  }
  &:focus-visible {
    outline: 3px solid rgba(27, 79, 214, 0.28);
    outline-offset: 2px;
  }
  .info-sala {
    padding: 1.55rem 1.7rem;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 0;
  }
  h3 {
    margin-bottom: 0.65rem;
    color: #2b1b17;
    text-shadow: none;
    font-size: 1.35rem;
  }
  p {
    color: #7e6f69;
    font-size: 0.95rem;
    min-height: 40px;
    text-shadow: none;
    margin: 0;
  }
  .ubicacion {
    min-height: auto;
    margin-top: 0.45rem;
    color: #5f4f4a;
    font-size: 0.9rem;
  }
  .equipaciones {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.45rem;
  }
  .equipacion-pill {
    background: #f5ede7;
    color: #5a463f;
    border: 1px solid #eadfd8;
    border-radius: 999px;
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
  }
}

.detalles {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.9rem 0 0.8rem;
  color: #5a463f;
}

.acciones-sala {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 0.45rem;
}

.acciones-botones {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.acciones-sala .precio {
  font-weight: 700;
  color: #362521;
  font-size: 1.35rem;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.boton-ver, .boton-info, .btn-nuevo, .btn-save {
  width: auto;
  padding: 0.7rem 1.1rem;
  background: #4b3e3b; 
  color: #fcfaf7;
  border: none;
  border-radius: 24px; 
  cursor: pointer;
  font-weight: 400;
  font-size: 0.95rem;
  letter-spacing: 0.02em;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.boton-ver {
  box-shadow: 0 6px 16px rgba(73, 57, 53, 0.14);
  font-weight: 600;
}

.boton-info {
  background: #f5ede7;
  box-shadow: 0 6px 16px rgba(54, 37, 33, 0.14);
  color: #362521;
  border: 1px solid #d9c7ba;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.boton-ver:hover, .btn-nuevo:hover, .btn-save:hover {
  background: #4a3530; /* Un punto más claro al pasar el cursor */
  box-shadow: 0 8px 18px rgba(54, 37, 33, 0.3);
}

.boton-info:hover {
  background: #eadfd8;
}

.icono-flecha {
  font-size: 1rem;
  line-height: 1;
  transition: transform 0.25s ease;
}

.boton-info:hover .icono-flecha {
  transform: translateX(3px);
}


.grupo-filtro {
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  align-items: flex-start;
  min-width: 0;
}

.grupo-filtro label {
  font-weight: 600;
  color: #2b1b17;
  font-size: 0.9rem;
}

.grupo-filtro input, .grupo-filtro select {
  width: 100%;
  padding: 0.75rem 0.85rem;
  border: 1px solid #e2d7cf;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  background-color: white;
  color: #2b1b17;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.grupo-filtro-ubicacion select:disabled {
  background: #f6efe9;
  color: #6e5e58;
  cursor: not-allowed;
  opacity: 1;
}

.nota-filtro-bloqueado {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: #7e6f69;
  text-shadow: none;
}

.equipamiento-filtro {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.equipamiento-opcion {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  color: #2b1b17;
  font-size: 0.95rem;
}

.equipamiento-opcion input {
  width: auto;
  margin: 0;
}

.limpiar-equipamiento {
  align-self: flex-start;
  margin-top: 0.25rem;
  padding: 0;
  border: none;
  background: transparent;
  color: #1b4fd6;
  font-size: 0.9rem;
  cursor: pointer;
}

.limpiar-equipamiento:hover {
  text-decoration: underline;
}

.sin-opciones {
  min-height: auto !important;
  color: #7e6f69;
  font-size: 0.9rem;
}

.grupo-filtro input:focus, .grupo-filtro select:focus {
  outline: none;
  border-color: #1b4fd6;
  box-shadow: 0 0 0 3px rgba(27, 79, 214, 0.14);
}

.sala-imagen {
  width: 100%;
  height: 100%;
  min-height: 250px;
  object-fit: cover;
  border-right: 1px solid #eee;
}

@media (max-width: 960px) {
  .home {
    height: auto;
    min-height: 100vh;
    overflow: visible;
  }

  .contenedor-principal {
    overflow: visible;
  }

  .catalogo-layout {
    grid-template-columns: 1fr;
    height: auto;
  }

  .grid-barrios {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sidebar-filtros {
    position: static;
    height: auto;
  }

  .panel-filtro,
  .contenido-catalogo {
    max-height: none;
    height: auto;
    overflow: visible;
  }

  .grid-salas {
    grid-auto-rows: auto;
    min-height: auto;
    gap: 1rem;
  }

  .tarjeta-sala {
    grid-template-columns: 1fr;
    height: auto;
  }

  .sala-imagen {
    min-height: 180px;
    border-right: none;
    border-bottom: 1px solid #eee;
  }

  .acciones-sala {
    align-items: flex-start;
    flex-direction: column;
  }

  .acciones-botones {
    justify-content: flex-start;
  }

  .boton-ver,
  .boton-info {
    width: fit-content;
  }
}

@media (max-width: 640px) {
  .hero {
    padding-top: 4.5rem;
  }

  .hero h1 {
    font-size: 2.35rem;
  }

  .selector-barrios h2 {
    font-size: 1.4rem;
  }

  .grid-barrios {
    grid-template-columns: 1fr;
  }
}

</style>