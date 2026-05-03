<template>
  <div class="home">
    <header class="hero">
      <h1>Catálogo de Salas para Equipos que <em>Avanzan</em></h1>
    </header>

    <section class="selector-barrios">
      <div class="intro-sedes">
        <span class="intro-kicker"> ESPACIOS CON IDENTIDAD PROPIA </span>
        <h2>Cuatro atmósferas urbanas. Tú eliges la <em>energía</em> de hoy.</h2>
      </div>

      <div class="intro-separador" aria-hidden="true"></div>

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

      <div v-if="sedeActiva" ref="catalogoPrincipal" class="contenedor-principal">
        <h2 class="titulo-catalogo-sede">Salas de {{ nombreSedeActiva }}</h2>
        <div class="catalogo-layout">
          <aside class="sidebar-filtros">
            <button
              type="button"
              class="filtros-mobile-toggle"
              @click="toggleFiltrosMovil"
              :aria-expanded="mostrarPanelFiltros ? 'true' : 'false'"
            >
              {{ mostrarPanelFiltros ? 'Ocultar filtros' : 'Mostrar filtros' }}
            </button>

            <transition name="desplegable-filtros">
              <div v-show="mostrarPanelFiltros" class="panel-filtro">
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
            </transition>
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
    </section>

    <!-- Sección ¿Por qué elegirnos? -->
    <section class="elegirnos-section">
      <div class="elegirnos-inner">
        <h2>¿Por qué elegirnos?</h2>
        <div class="elegirnos-grid">
          <div class="caja-elegirnos">
            <i class="fa-solid fa-mug-hot icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Café de especialidad</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-laptop icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Material necesario para clientes</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-key icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Acceso 24/7</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-broom icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Limpieza diaria</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-user-group icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Networking mensual</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-video icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Cámaras de seguridad</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-wifi icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Internet de alta velocidad</span>
          </div>
          <div class="caja-elegirnos">
            <i class="fa-solid fa-headset icono-elegirnos" aria-hidden="true"></i>
            <span class="concepto-elegirnos">Soporte en recepción</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Sección de Opiniones / Testimonios -->
    <section class="opiniones-section">
      <div class="opiniones-inner">
        <h2>Opiniones de nuestros coworkers</h2>
        
        <div class="carrusel-wrapper">
          <button 
            type="button" 
            class="carrusel-control prev" 
            @click="anteriorSlide" 
            :disabled="slideActual === 0"
            aria-label="Opiniones anteriores"
          >
            ‹
          </button>
          
          <div class="carrusel-contenedor">
            <div class="carrusel-track" :style="{ transform: `translateX(-${slideActual * 100}%)` }">
              <div 
                class="carrusel-slide" 
                v-for="(grupo, idx) in gruposOpiniones" 
                :key="idx"
              >
                <div 
                  class="caja-opinion" 
                  v-for="opinion in grupo" 
                  :key="opinion.id"
                >
                  <div class="estrellas">
                    <span v-for="n in opinion.estrellas" :key="n">★</span>
                  </div>
                  <p class="opinion-texto">"{{ opinion.texto }}"</p>
                  <div class="opinion-autor">
                    <strong>{{ opinion.autor }}</strong>
                    <span>{{ opinion.puesto }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button 
            type="button" 
            class="carrusel-control next" 
            @click="siguienteSlide" 
            :disabled="slideActual === gruposOpiniones.length - 1"
            aria-label="Opiniones siguientes"
          >
            ›
          </button>
        </div>

        <div class="carrusel-indicadores">
          <button 
            v-for="(grupo, idx) in gruposOpiniones" 
            :key="idx" 
            :class="['indicador', { activo: slideActual === idx }]"
            @click="irASlide(idx)"
            :aria-label="`Ir al grupo ${idx + 1}`"
          ></button>
        </div>

        <!-- Formulario para agregar reseña -->
        <div class="divisor-resena"></div>
        
        <div class="formulario-resena-contenedor">
          <h3>Déjanos tu opinión</h3>
          <p class="intro-formulario">¿Eres coworker o has reservado alguna de nuestras salas? Comparte tu experiencia con la comunidad.</p>
          
          <form @submit.prevent="publicarResena" class="formulario-resena">
            <div class="estrellas-selector-wrap">
              <span class="label-estrellas">Tu valoración:</span>
              <div class="estrellas-rating">
                <button
                  type="button"
                  v-for="n in 5"
                  :key="n"
                  class="estrella-btn"
                  :class="{ activa: n <= (hoverEstrellas || nuevaResena.estrellas) }"
                  @mouseenter="hoverEstrellas = n"
                  @mouseleave="hoverEstrellas = 0"
                  @click="nuevaResena.estrellas = n"
                  :aria-label="`Valorar con ${n} estrellas`"
                >
                  ★
                </button>
              </div>
            </div>

            <div class="campos-grupo">
              <div class="campo-item">
                <label for="resena-autor">Nombre completo</label>
                <input
                  id="resena-autor"
                  v-model="nuevaResena.autor"
                  type="text"
                  placeholder="Ej. Laura Gómez"
                  required
                />
              </div>

              <div class="campo-item">
                <label for="resena-puesto">Puesto / Empresa</label>
                <input
                  id="resena-puesto"
                  v-model="nuevaResena.puesto"
                  type="text"
                  placeholder="Ej. Diseñadora Freelance"
                  required
                />
              </div>
            </div>

            <div class="campo-item texto-item">
              <label for="resena-texto">Comentario</label>
              <textarea
                id="resena-texto"
                v-model="nuevaResena.texto"
                rows="4"
                placeholder="Cuéntanos qué es lo que más te gusta de CoWorkFlow..."
                required
              ></textarea>
            </div>

            <div class="acciones-form-resena">
              <button type="submit" class="btn-publicar" :disabled="publicandoResena">
                <span v-if="publicandoResena" class="cargando-spinner"></span>
                <span>Publicar reseña</span>
              </button>
            </div>

            <transition name="fade">
              <div>
                <p v-if="errorResena" class="resena-error-msg">{{ errorResena }}</p>
                <p v-else-if="exitoResena" class="resena-success-msg">{{ exitoResena }}</p>
              </div>
            </transition>
          </form>
        </div>
      </div>
    </section>

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
      cargando: true,
      esMovil: false,
      filtrosMovilAbierto: false,
      slideActual: 0,
      opiniones: [],
      nuevaResena: {
        autor: '',
        puesto: '',
        texto: '',
        estrellas: 5
      },
      publicandoResena: false,
      errorResena: null,
      exitoResena: null,
      hoverEstrellas: 0
    }
  },
  mounted() {
    this.actualizarModoMovil();
    window.addEventListener('resize', this.actualizarModoMovil);

    // Si el usuario está logueado, pre-rellenar el autor
    const userObj = this.$store.getters.getUser;
    if (userObj && userObj.nombre_completo) {
      this.nuevaResena.autor = userObj.nombre_completo;
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.actualizarModoMovil);
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

    // Traer reseñas desde el backend
    try {
      const resenasResponse = await axios.get('http://localhost:8000/api/resenas/');
      this.opiniones = resenasResponse.data;
    } catch (error) {
      console.error("Error al traer reseñas:", error);
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
    toggleFiltrosMovil() {
      if (!this.esMovil) return;
      this.filtrosMovilAbierto = !this.filtrosMovilAbierto;
    },
    actualizarModoMovil() {
      const eraMovil = this.esMovil;
      this.esMovil = window.innerWidth <= 960;

      if (!this.esMovil) {
        this.filtrosMovilAbierto = true;
      } else if (!eraMovil) {
        this.filtrosMovilAbierto = false;
      }
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
    },
    siguienteSlide() {
      if (this.slideActual < this.gruposOpiniones.length - 1) {
        this.slideActual++;
      }
    },
    anteriorSlide() {
      if (this.slideActual > 0) {
        this.slideActual--;
      }
    },
    irASlide(idx) {
      this.slideActual = idx;
    },
    async publicarResena() {
      this.errorResena = null;
      this.exitoResena = null;

      if (!this.nuevaResena.autor.trim() || !this.nuevaResena.puesto.trim() || !this.nuevaResena.texto.trim()) {
        this.errorResena = "Todos los campos son obligatorios.";
        return;
      }

      this.publicandoResena = true;
      try {
        const respuesta = await axios.post('http://localhost:8000/api/resenas/', {
          autor: this.nuevaResena.autor,
          puesto: this.nuevaResena.puesto,
          texto: this.nuevaResena.texto,
          estrellas: this.nuevaResena.estrellas
        });

        this.opiniones.push(respuesta.data.resena);
        this.exitoResena = "¡Reseña publicada con éxito! Gracias por tu comentario.";

        // Limpiar formulario y restablecer valores
        this.nuevaResena.texto = '';
        this.nuevaResena.puesto = '';
        this.nuevaResena.estrellas = 5;

        const userObj = this.$store.getters.getUser;
        if (userObj && userObj.nombre_completo) {
          this.nuevaResena.autor = userObj.nombre_completo;
        } else {
          this.nuevaResena.autor = '';
        }

        // Ir al último slide
        this.$nextTick(() => {
          this.slideActual = this.gruposOpiniones.length - 1;
        });

        setTimeout(() => {
          this.exitoResena = null;
        }, 5000);

      } catch (err) {
        console.error("Error al publicar reseña:", err);
        if (err.response && err.response.data) {
          this.errorResena = err.response.data.message || "Error al publicar la reseña.";
        } else {
          this.errorResena = "No se pudo conectar con el servidor.";
        }
      } finally {
        this.publicandoResena = false;
      }
    }
  },
  computed: {
    nombreSedeActiva() {
      if (!this.sedeActiva) return '';

      const sede = this.sedesMapeadas.find(item => item.location === this.sedeActiva);
      if (sede?.barrio) return sede.barrio;

      return this.sedeActiva;
    },
    gruposOpiniones() {
      const grupos = [];
      for (let i = 0; i < this.opiniones.length; i += 3) {
        grupos.push(this.opiniones.slice(i, i + 3));
      }
      return grupos;
    },
    mostrarPanelFiltros() {
      return !this.esMovil || this.filtrosMovilAbierto;
    },
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
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');

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
  color: #2b1b17;
  text-shadow: none;
  padding: 5.25rem 2rem 1.8rem;
  text-align: center;
  flex-shrink: 0;
}

  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.35rem, 5vw, 4.5rem);
    font-weight: 400;
    letter-spacing: -0.02em;
    margin: 0 auto;
    margin-bottom: 30px;
    line-height: 1.2;
    max-width: none;
    width: fit-content;
    color: #fff;
    text-shadow: 0 8px 48px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
    border: 2.5px solid #fff;
    border-radius: 1.8em;
    padding: 0.25em 1.2em;
    display: inline-block;
    background: rgba(0,0,0,0.10);
    box-shadow: 0 2px 16px 0 rgba(0,0,0,0.18);
  }

.hero h1::after {
  content: '';
  display: block;
  width: min(380px, 72vw);
  height: 1px;
  margin: 1rem auto 0;
  background: linear-gradient(90deg, rgba(122, 90, 74, 0.06), rgba(122, 90, 74, 0.55), rgba(122, 90, 74, 0.06));
}

.hero h1 em {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-weight: 400;
}

.selector-barrios {
  max-width: 100%;
  margin: 0 auto;
  width: 100%;
  padding: 0 1.25rem 1.5rem;
  color: #2b1b17;
  text-shadow: none;
}

.intro-sedes {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  margin: 0 auto 1.25rem;
  width: 100%;
}

.intro-kicker {
  display: inline-block;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.98rem;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 6px 32px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
}

  .intro-sedes h2 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.9rem, 2.7vw, 2.85rem);
  line-height: 1.22;
  margin: 0;
    color: #fff;
    font-weight: 500;
    max-width: none;
    width: 100%;
    text-shadow: 0 8px 48px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
}

.intro-sedes h2 em {
  font-style: italic;
  font-weight: 400;
}

.intro-descripcion {
  margin: 0;
  color: #5b4a44;
  font-size: 1.02rem;
  line-height: 1.78;
  text-shadow: none;
  max-width: none;
  width: 100%;
}

.intro-separador {
  width: min(1140px, 100%);
  height: 2.5px;
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0.08) 0%,
    rgba(255,255,255,0.85) 40%,
    rgba(255,255,255,0.08) 100%
  );
  margin: 0 auto 1.5rem;
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.45);
}

.grid-barrios {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 3.2rem;
  row-gap: 2.65rem;
  margin: 4rem auto 0;
  max-width: 1380px;
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
  padding: 1rem 1rem 1rem 3.25rem;
  background: linear-gradient(180deg, rgba(25, 15, 11, 0.1) 28%, rgba(18, 10, 7, 0.82) 100%);

  h3 {
    margin: 0;
    font-size: 2.0rem;
    color: #fff;
  }

  p {
    margin: 0;
    font-size: 1rem;
    line-height: 1.4;
    color: #efe2da;
    min-height: auto;
  }
}

.barrio-kicker {
  font-size: 0.85rem;
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
  font-size: 0.9rem;
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
  border: 1px solid #c8b2a6;
  color: #4c3a33;
  background: rgba(255, 255, 255, 0.65);
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
  padding: 6.75rem 1.25rem 2rem;
  width: 100%;
  min-height: auto;
  overflow: visible;
}

  .titulo-catalogo-sede {
    margin: 0 0 1.15rem;
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.65rem, 2.3vw, 2.4rem);
    font-weight: 600;
    color: #fff;
    letter-spacing: -0.01em;
    text-shadow: 0 8px 48px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
    border: 2.5px solid #fff;
    border-radius: 1.8em;
    padding: 0.25em 1.2em;
    display: inline-block;
    background: rgba(0,0,0,0.10);
    box-shadow: 0 2px 16px 0 rgba(0,0,0,0.18);
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

.filtros-mobile-toggle {
  display: none;
  width: 100%;
  border: 1px solid #e2d7cf;
  background: #ffffff;
  color: #2b1b17;
  border-radius: 10px;
  padding: 0.72rem 0.9rem;
  font-size: 0.96rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  box-shadow: 0 5px 14px rgba(43, 27, 23, 0.06);
}

.desplegable-filtros-enter-active,
.desplegable-filtros-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
  transform-origin: top;
}

.desplegable-filtros-enter-from,
.desplegable-filtros-leave-to {
  opacity: 0;
  transform: translateY(-8px);
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
    max-width: 100%;
  }

  .sidebar-filtros {
    position: static;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .filtros-mobile-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;
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

  .intro-sedes h2 {
    font-size: 1.7rem;
  }

  .intro-descripcion {
    font-size: 0.97rem;
    line-height: 1.7;
  }

  .grid-barrios {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .intro-descripcion {
    max-width: 100%;
    font-size: 0.97rem;
    line-height: 1.65;
  }
}

/* --- SECCIÓN ¿POR QUÉ ELEGIRNOS? --- */
.elegirnos-section {
  max-width: 80%;
  margin: 6rem auto 0;
  width: 100%;
  padding: 0 1.25rem;
  text-align: center;
  color: #2b1b17;
  text-shadow: none;
}
  .elegirnos-inner h2 {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
    color: #fff;
    text-shadow: 0 8px 48px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
}

.elegirnos-inner h2::before,
.elegirnos-inner h2::after {
  content: '';
  height: 2.5px;
  flex: 1 1 220px;
  max-width: 360px;
  background: linear-gradient(90deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.85) 40%, rgba(255,255,255,0.08) 100%);
  box-shadow: 0 2px 16px 0 rgba(0,0,0,0.45);
}
.elegirnos-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.5rem;
}
@media (max-width: 900px) {
  .elegirnos-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (max-width: 600px) {
  .elegirnos-inner h2::before,
  .elegirnos-inner h2::after {
    max-width: 90px;
  }

  .elegirnos-grid {
    grid-template-columns: 1fr;
  }
}
.caja-elegirnos {
  padding: 2rem 1.5rem;
  border: 1px solid #4b3a33;
  background: rgba(247, 243, 237, 0.97);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 8px 8px 0 rgba(43, 27, 23, 0.1);
  transition: transform 0.25s ease, box-shadow 0.25s ease, background-color 0.25s ease;
  text-shadow: none !important;
}
.caja-elegirnos:hover {
  transform: translateY(-5px);
  box-shadow: 12px 12px 20px rgba(43, 27, 23, 0.2);
  background: #ffffff;
}
.icono-elegirnos {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #7a5849;
}
.concepto-elegirnos {
  font-family: 'Playfair Display', serif;
  color: #2b1b17;
  font-size: 1.16rem;
  font-weight: 500;
  line-height: 1.3;
}

/* --- SECCIÓN OPINIONES (CARRUSEL DE TRES EN TRES) --- */
.opiniones-section {
  max-width: 1320px;
  margin: 4rem auto 4rem;
  width: 100%;
  padding: 4rem 1.25rem;
  text-align: center;
  color: #2b1b17;
  text-shadow: none;
}
  .opiniones-inner h2 {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  font-weight: 600;
    color: #fff;
    text-shadow: 0 8px 48px rgba(0,0,0,0.95), 0 2px 8px #000, 0 1px 0 #000;
}
.carrusel-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}
.carrusel-contenedor {
  overflow: hidden;
  width: 100%;
}
.carrusel-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
  width: 100%;
}
.carrusel-slide {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.5rem;
  width: 100%;
  flex-shrink: 0;
  padding: 0.5rem;
}
@media (max-width: 900px) {
  .carrusel-slide {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
.caja-opinion {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 2.2rem 1.8rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 8px 32px 0 rgba(31, 15, 10, 0.15);
  transition: transform 0.3s ease, border-color 0.3s ease;
  text-shadow: none !important;
  color: #2b1b17;
  background-color: rgba(253, 248, 244, 0.95);
}
.caja-opinion:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.6);
}
.estrellas {
  color: #d48c3f;
  font-size: 1.1rem;
  margin-bottom: 0.85rem;
}
.opinion-texto {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #4b3b35;
  margin-bottom: 1.5rem;
  font-style: italic;
  min-height: auto !important;
}
.opinion-autor {
  display: flex;
  flex-direction: column;
}
.opinion-autor strong {
  font-size: 1.05rem;
  color: #1e110c;
}
.opinion-autor span {
  font-size: 0.82rem;
  color: #8c7367;
  margin-top: 0.15rem;
}
.carrusel-control {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid #d8c6bb;
  color: #5a3f33;
  font-size: 2rem;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.25s, transform 0.25s;
  backdrop-filter: blur(4px);
  user-select: none;
}
.carrusel-control:hover:not(:disabled) {
  background: #ffffff;
  transform: scale(1.05);
}
.carrusel-control:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
.carrusel-indicadores {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}
.indicador {
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
  border: none;
  background: rgba(84, 55, 43, 0.3);
  cursor: pointer;
  transition: background 0.25s, transform 0.25s;
}
.indicador.activo {
  background: #5a3f33;
  transform: scale(1.2);
}

/* --- DIVISOR Y FORMULARIO DE RESEÑAS --- */
.divisor-resena {
  width: min(800px, 100%);
  height: 1.5px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 0%, rgba(90, 63, 51, 0.25) 50%, rgba(255, 255, 255, 0.05) 100%);
  margin: 3.5rem auto 3rem;
}

.formulario-resena-contenedor {
  max-width: 800px;
  margin: 0 auto;
  padding: 2.5rem;
  background: rgba(253, 248, 244, 0.95);
  border: 1px solid #eaddd3;
  border-radius: 20px;
  box-shadow: 0 12px 36px rgba(43, 27, 23, 0.06);
  text-align: left;
  text-shadow: none !important;

  h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: #2b1b17;
    margin: 0 0 0.5rem;
    font-weight: 600;
  }

  .intro-formulario {
    color: #7e6f69;
    font-size: 0.96rem;
    margin: 0 0 2rem;
    line-height: 1.5;
  }
}

.formulario-resena {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.estrellas-selector-wrap {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.label-estrellas {
  font-weight: 600;
  color: #2b1b17;
  font-size: 0.95rem;
}

.estrellas-rating {
  display: flex;
  gap: 0.35rem;
}

.estrella-btn {
  background: none;
  border: none;
  font-size: 1.85rem;
  color: #e2d7cf;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: transform 0.15s ease, color 0.15s ease;

  &:hover {
    transform: scale(1.15);
  }

  &.activa {
    color: #d48c3f;
  }
}

.campos-grupo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

@media (max-width: 600px) {
  .campos-grupo {
    grid-template-columns: 1fr;
  }
  .formulario-resena-contenedor {
    padding: 1.5rem;
  }
}

.campo-item {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;

  label {
    font-weight: 600;
    color: #2b1b17;
    font-size: 0.9rem;
  }

  input, textarea {
    width: 100%;
    padding: 0.78rem 0.95rem;
    border: 1px solid #e2d7cf;
    border-radius: 8px;
    font-size: 0.96rem;
    font-family: inherit;
    background-color: white;
    color: #2b1b17;
    box-sizing: border-box;
    transition: border-color 0.25s, box-shadow 0.25s;

    &:focus {
      outline: none;
      border-color: #1b4fd6;
      box-shadow: 0 0 0 3px rgba(27, 79, 214, 0.12);
    }
  }

  textarea {
    resize: vertical;
  }
}

.acciones-form-resena {
  display: flex;
  justify-content: flex-end;
}

.btn-publicar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.82rem 1.8rem;
  background: #362521;
  color: #fcfaf7;
  border: none;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.98rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(54, 37, 33, 0.15);
  transition: background-color 0.25s, transform 0.2s, box-shadow 0.25s;

  &:hover:not(:disabled) {
    background: #4a3530;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(54, 37, 33, 0.25);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.cargando-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.resena-error-msg {
  color: #b42318;
  font-size: 0.9rem;
  margin: 0.5rem 0 0;
  text-align: center;
  font-weight: 500;
}

.resena-success-msg {
  color: #027a48;
  font-size: 0.9rem;
  margin: 0.5rem 0 0;
  text-align: center;
  font-weight: 500;
}

/* Transición fade para mensajes */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>