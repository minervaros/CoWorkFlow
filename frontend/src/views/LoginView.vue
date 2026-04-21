<template>
  <div class="login-container">
    <form @submit.prevent="manejarLogin" class="formulario-login">
      <h2>Bienvenido a CoWorkFlow</h2>
      <p>Introduce tus credenciales para acceder</p>

      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" placeholder="ejemplo@correo.com" required />
      </div>

      <div class="form-group">
        <label>Contraseña</label>
        <input v-model="password" type="password" placeholder="********" required />
      </div>

      <button type="submit" class="btn-login">Entrar</button>
      
      <p v-if="error" class="error-msg">{{ error }}</p>
    </form>
  </div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async manejarLogin() {
      this.error = null; // Limpiamos errores previos
      
      try {
        // 1. Enviamos la petición al backend (Flask corre en el 8000)
        const respuesta = await axios.post('http://localhost:8000/api/auth/login', {
          email: this.email,
          password: this.password
        });

        // 2. Si el login es correcto, guardamos los datos en la "caja fuerte" (Vuex)
        // Usamos 'dispatch' para llamar a la acción que creamos en el Store
        await this.$store.dispatch('saveLogin', {
          token: respuesta.data.access_token,
          user: {
            email: this.email,
            role: respuesta.data.user.role // Si tu backend lo devuelve
          }
        });

        console.log("¡Login exitoso!");

        // 3. Redirigimos al usuario a la página de inicio
        this.$router.push('/');

      } catch (err) {
        // 4. Si hay un error (401, 404, 500...), lo mostramos
        if (err.response && err.response.data) {
          this.error = err.response.data.message || "Credenciales incorrectas";
        } else {
          this.error = "No se pudo conectar con el servidor";
        }
        console.error("Error en el login:", err);
      }
    }
  }
}
</script>

<style lang="scss" scoped>

$color-primario: #42b983;
$color-oscuro: #2c3e50;
$color-error: #e74c3c;

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;

  .formulario-login {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;

    h2 {
      color: $color-oscuro;
      margin-bottom: 0.5rem;
    }

    .form-group {
      margin-bottom: 1.5rem;
      text-align: left;

      label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
      }

      input {
        width: 100%;
        padding: 0.8rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        box-sizing: border-box; // Para que el padding no ensanche el input

        &:focus {
          outline: none;
          border-color: $color-primario;
        }
      }
    }

    .btn-login {
      width: 100%;
      padding: 1rem;
      background-color: $color-primario;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 1rem;
      font-weight: bold;
      cursor: pointer;
      transition: background 0.3s;

      &:hover {
        background-color: darken($color-primario, 10%);
      }
    }

    .error-msg {
      color: $color-error;
      margin-top: 1rem;
      font-size: 0.9rem;
    }
  }
}
</style>