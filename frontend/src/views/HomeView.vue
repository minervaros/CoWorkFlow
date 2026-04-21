<template>
  <div class="home">
    <header class="hero">
      <h1>Encuentra tu espacio de trabajo</h1>
      <p>Salas equipadas para tus reuniones o sesiones de concentración.</p>
    </header>

    <div class="contenedor-principal">
      <div v-if="cargando" class="spinner">Cargando salas disponibles...</div>
      
      <div v-else-if="salasVisibles.length === 0" class="sin-salas">
        No hay salas disponibles en este momento.
      </div>

      <div v-else class="grid-salas">
        <div v-for="sala in salasVisibles" :key="sala.id" class="tarjeta-sala">
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
      // Solo mostramos las salas que tengan is_active === true
      return this.salas.filter(sala => sala.is_active === true);
    }
  }
}
</script>

<style lang="scss" scoped>
.hero { background: #2c3e50; color: white; padding: 4rem 2rem; text-align: center; }
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

.boton-ver {
  width: 100%;
  padding: 0.8rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  &:hover { background: #2980b9; }
}
</style>