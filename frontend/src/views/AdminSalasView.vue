<template>
  <div class="admin-salas">
    <div class="header">
      <h1>Gestión de Espacios</h1>
      <button @click="abrirModalCrear" class="btn-nuevo">+ Nueva Sala</button>
    </div>

    <div class="tabla-contenedor">
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Capacidad</th>
            <th>Precio/h</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sala in salas" :key="sala.id">
            <td><strong>{{ sala.name }}</strong></td>
            <td>{{ sala.capacity }} personas</td>
            <td>{{ sala.price_per_hour }}€</td>
            <td>
              <span :class="['status-pill', sala.is_active ? 'activo' : 'inactivo']">
                {{ sala.is_active ? 'Activa' : 'Fuera de servicio' }}
              </span>
            </td>
            <td>
              <button @click="abrirModalEditar(sala)" class="btn-edit">Editar</button>
              <button @click="alternarEstado(sala)" class="btn-toggle">
                {{ sala.is_active ? 'Desactivar' : 'Activar' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="mostrarModal" class="modal-overlay">
      <div class="modal">
        <h2>{{ editando ? 'Editar Sala' : 'Nueva Sala' }}</h2>
        <form @submit.prevent="guardarSala">
          <input v-model="form.name" placeholder="Nombre de la sala" required />
          <input v-model.number="form.capacity" type="number" placeholder="Capacidad" required />
          <input v-model.number="form.price_per_hour" type="number" step="0.01" placeholder="Precio por hora" required />
          <textarea v-model="form.description" placeholder="Descripción de la sala"></textarea>
          
          <div class="grupo-form">
            <label>🔗 URL de la Imagen:</label>
            <input v-model="form.image_url" type="text" placeholder="Pegue el enlace de la foto (Unsplash, Pexels...)" />
          </div>

          <div class="modal-btns">
            <button type="button" @click="mostrarModal = false">Cancelar</button>
            <button type="submit" class="btn-save">Guardar Cambios</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      salas: [],
      mostrarModal: false,
      editando: false,
      form: { id: null, name: '', capacity: null, price_per_hour: null, description: '' },

      nuevaSala: {
        name: '',
        description: '',
        capacity: 0,
        price_per_hour: 0,
        image_url: '' // <--- AÑADE ESTA LÍNEA AQUÍ
      }
    };
  },
  async created() {
    this.cargarSalas();
  },
  methods: {
    async cargarSalas() {
      const token = localStorage.getItem('user-token');
      try {
        // Forzamos al backend a que NO filtre por activas
        const res = await axios.get('http://localhost:8000/api/rooms/?active_only=false', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.salas = res.data;
      } catch (e) {
        console.error("Error al cargar salas en admin", e);
      }
    },
    abrirModalCrear() {
      this.editando = false;
      this.form = { id: null, name: '', capacity: null, price_per_hour: null, description: '' };
      this.mostrarModal = true;
    },
    abrirModalEditar(sala) {
      this.editando = true;
      this.form = { ...sala };
      this.mostrarModal = true;
    },
    async guardarSala() {
      const token = localStorage.getItem('user-token');
      try {
        if (this.editando) {
          await axios.put(`http://localhost:8000/api/rooms/${this.form.id}`, this.form, {
            headers: { Authorization: `Bearer ${token}` }
          });
        } else {
          await axios.post('http://localhost:8000/api/rooms/', this.form, {
            headers: { Authorization: `Bearer ${token}` }
          });
        }
        this.mostrarModal = false;
        this.cargarSalas();
      } catch (e) { alert("Error al guardar la sala"); }
    },
    async alternarEstado(sala) {
      const nuevoEstado = !sala.is_active;
      const token = localStorage.getItem('user-token');
      try {
        await axios.put(`http://localhost:8000/api/rooms/${sala.id}`, { is_active: nuevoEstado }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        sala.is_active = nuevoEstado;
      } catch (e) { alert("Error al cambiar estado"); }
    }
  }
};
</script>

<style scoped>
.admin-salas { padding: 2rem; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.btn-nuevo { background: #27ae60; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; }

.status-pill { padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; }
.status-pill.activo { background: #e1f7e7; color: #27ae60; }
.status-pill.inactivo { background: #fdeaea; color: #eb5757; }

/* Estilos del Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal { background: white; padding: 2rem; border-radius: 12px; width: 400px; display: flex; flex-direction: column; gap: 1rem; }
.modal input, .modal textarea { padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
.btn-save { background: #3498db; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
</style>