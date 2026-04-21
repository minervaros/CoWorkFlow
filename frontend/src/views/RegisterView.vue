<template>
  <div class="contenedor-registro">
    <div class="tarjeta-registro">
      <h2>Crea tu cuenta</h2>
      <p>Únete a la comunidad de CoWorkflow</p>

      <form @submit.prevent="manejarRegistro" class="formulario-registro">
        <div class="campo">
          <label>Nombre completo</label>
          <input v-model="nombre" type="text" placeholder="Tu nombre" required>
        </div>

        <div class="campo">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="email@ejemplo.com" required>
        </div>

        <div class="campo">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" required>
        </div>

        <button type="submit" class="boton-registro">Registrarse</button>
      </form>

      <p v-if="error" class="mensaje-error">{{ error }}</p>
      
      <p class="enlace-login">
        ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      nombre: '',
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async manejarRegistro() {
      this.error = null;
      try {
        // Llamada a la ruta que definiste en tu Blueprint de Flask
        await axios.post('http://localhost:8000/api/auth/register', {
          full_name: this.nombre, // Asegúrate de que coincida con lo que espera tu modelo
          email: this.email,
          password: this.password
        });

        // Si el registro es exitoso, lo mandamos al login para que entre
        alert("¡Cuenta creada con éxito! Ahora puedes iniciar sesión.");
        this.$router.push('/login');

      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data.message || "Error al registrarse";
        } else {
          this.error = "No se pudo conectar con el servidor";
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
/* Puedes reutilizar los estilos del login para mantener la estética */
.contenedor-registro {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}
.tarjeta-registro {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
.campo {
  margin-bottom: 1.2rem;
  text-align: left;
  label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
  input { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 6px; }
}
.boton-registro {
  width: 100%;
  padding: 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.mensaje-error { color: #ff5252; margin-top: 1rem; }
.enlace-login { margin-top: 1.5rem; font-size: 0.9rem; }
</style>