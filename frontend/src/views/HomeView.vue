<template>
  <div class="home">
    <header class="hero">
      <h1>Espacios de Trabajo Creados para <em>Inspirar</em></h1>
  <p>Creemos en entornos que no siguen tendencias, sino que trascienden. Diseñados para la concentración, anclados para el éxito.</p>
    </header>

    <div class="filtros-home">
      <div class="grupo-filtro">
        <label>🔍 Buscar sala:</label>
        <input v-model="busquedaNombre" type="text" placeholder="Ej: Sala de Juntas, Podcast..." />
      </div>
      
      <div class="grupo-filtro">
        <label>👥 Capacidad mínima:</label>
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
    </div>

    <div class="contenedor-principal">
      <div v-if="cargando" class="spinner">Cargando salas disponibles...</div>
      
      <div v-else-if="salasVisibles.length === 0" class="sin-salas">
        <p>No hay salas disponibles en este momento. Vuelve más tarde.</p>
      </div>

      <div v-else class="grid-salas">
        <div v-for="sala in salasVisibles" :key="sala.id" class="tarjeta-sala">

          <img 
            :src="sala.image_url || 'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=500'" 
            alt="Foto de la sala" 
            class="sala-imagen"
          />

          <div class="info-sala">
            <h3>{{ sala.name }}</h3>
            <p>{{ sala.description }}</p>
            <div class="detalles">
              <span>👤 Capacidad: {{ sala.capacity }}</span>
              <span class="precio">{{ sala.price_per_hour }}€/h</span>
            </div>
            <button @click="irAReservar(sala)" class="boton-ver">
              Reservar ahora
            </button>
          </div>
        </div>
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
      busquedaNombre: '',
      capacidadMinima: 0,
      cargando: true
    }
  },
  async created() {
    // Al cargar la página, pedimos las salas al backend
    try {
      const response = await axios.get('http://localhost:8000/api/rooms/');
      this.salas = response.data;
    } catch (error) {
      console.error("Error al traer salas:", error);
    } finally {
      this.cargando = false;
    }
  },
  methods: {
    irAReservar(sala) {
      // Pasamos el ID y el nombre por la URL para que ReservasView lo reciba
      this.$router.push({
        path: '/reservas',
        query: { sala: sala.id, nombre: sala.name }
      });
    }
  },
  computed: {
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

      return resultado;
    }
  }
}
</script>

<style lang="scss" scoped>
.hero {
  background: #fcfaf7;
  color: #2b1b17;
  padding: 6rem 2rem 4rem 2rem;
  text-align: center;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem;
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
  font-size: 1.1rem;
  color: #6e5e58; /* Marrón ceniza suave */
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}
.contenedor-principal { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.grid-salas { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }

.tarjeta-sala {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.3s;
  &:hover { transform: translateY(-5px); }
  .info-sala { padding: 1.5rem; text-align: left; }
  h3 { margin-bottom: 0.5rem; color: #2c3e50; }
  p { color: #7f8c8d; font-size: 0.9rem; min-height: 40px; }
}

.detalles {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1.5rem 0;
  .precio { font-weight: bold; color: #42b983; font-size: 1.2rem; }
}

.boton-ver, .btn-nuevo, .btn-save {
  width: 100%;
  padding: 1rem;
  background: #362521; /* El color café oscuro de la imagen */
  color: #fcfaf7;
  border: none;
  border-radius: 24px !important; /* Botón completamente ovalado como el de la foto */
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  letter-spacing: 0.02em;
  transition: background-color 0.3s;
}

.boton-ver:hover, .btn-nuevo:hover, .btn-save:hover {
  background: #4a3530; /* Un punto más claro al pasar el cursor */
}


.filtros-home {
  max-width: 1200px;
  margin: 2rem auto 0 auto;
  padding: 0 2rem;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.grupo-filtro {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-start;
  flex: 1;
  min-width: 250px;
}

.grupo-filtro label {
  font-weight: bold;
  color: #34495e;
  font-size: 0.9rem;
}

.grupo-filtro input, .grupo-filtro select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
  transition: border-color 0.3s;
}

.grupo-filtro input:focus, .grupo-filtro select:focus {
  outline: none;
  border-color: #3498db;
}

.sala-imagen {
  width: 100%;
  height: 200px;
  object-fit: cover; /* Hace que la foto se adapte sin deformarse */
  border-bottom: 1px solid #eee;
}

</style>