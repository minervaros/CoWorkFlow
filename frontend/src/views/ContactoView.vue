<template>
  <div :class="['contacto-view', { 'modo-modal': enModal }]">
    <div class="contacto-wrap">
      <div class="contacto-card">
        <aside class="contacto-panel">
          <div class="contacto-panel-content">
            <p class="contacto-kicker">Soporte CoWorkFlow</p>
            <h1>Contacto</h1>
            <p>Cuéntanos tu duda y te enviaremos una confirmación por correo.</p>
          </div>
          <img :src="require('@/assets/cowork-illustration.png')" alt="Equipo en coworking" class="contacto-illustration" />
        </aside>

        <form class="contacto-form" @submit.prevent="enviarFormulario">
            <div class="contacto-titulo-movil">Contacto</div>
          <div class="campo">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model.trim="form.nombre" type="text" placeholder="Ej: Nombre Apellido" required maxlength="120" />
          </div>

          <div class="campo">
            <label for="email">Email</label>
            <input id="email" v-model.trim="form.email" type="email" placeholder="Ej: ana@correo.com" required maxlength="180" />
          </div>

          <div class="campo">
            <label for="asunto">Asunto</label>
            <input id="asunto" v-model.trim="form.asunto" type="text" placeholder="Ej: Información sobre reservas" required maxlength="180" />
          </div>

          <div class="campo">
            <label for="mensaje">Mensaje</label>
            <textarea id="mensaje" v-model.trim="form.mensaje" rows="6" placeholder="Cuéntanos en qué podemos ayudarte" required maxlength="5000"></textarea>
          </div>

          <div class="acciones">
            <button class="btn-principal" type="submit" :disabled="enviando">
              {{ enviando ? 'Enviando...' : 'Enviar' }}
            </button>
          </div>

          <p v-if="estado.mensaje" :class="['feedback', estado.tipo]">{{ estado.mensaje }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ContactoView',
  props: {
    enModal: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      enviando: false,
      form: {
        nombre: '',
        email: '',
        asunto: '',
        mensaje: ''
      },
      estado: {
        tipo: '',
        mensaje: ''
      }
    };
  },
  created() {
    const user = this.$store?.state?.user;
    if (user?.full_name) this.form.nombre = user.full_name;
    if (user?.email) this.form.email = user.email;
  },
  methods: {
    async enviarFormulario() {
      this.estado = { tipo: '', mensaje: '' };
      this.enviando = true;

      try {
        const response = await axios.post('http://localhost:8000/api/contact/send', this.form);
        this.estado = {
          tipo: 'ok',
          mensaje: response.data?.message || 'Mensaje enviado correctamente.'
        };
        this.form.asunto = '';
        this.form.mensaje = '';
      } catch (error) {
        this.estado = {
          tipo: 'error',
          mensaje: error?.response?.data?.message || 'No se pudo enviar el mensaje.'
        };
      } finally {
        this.enviando = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
// Título pequeño solo para móvil
.contacto-titulo-movil {
  display: none;
  text-align: center;
  font-size: 1.08rem;
  color: #6d534d;
  font-weight: 700;
  letter-spacing: 0.04em;
  margin-bottom: 0.7rem;
}

@media (max-width: 860px) {
  .contacto-titulo-movil {
    display: block;
  }
}


.contacto-card {
  display: grid;
  grid-template-columns: minmax(120px, 0.5fr) minmax(340px, 1fr);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #d6bca9;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  text-shadow: none;
}

.contacto-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  overflow: hidden;
  min-height: 120px;
  padding: 0.7rem 0.7rem 0.7rem 0.7rem;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(66, 41, 33, 0.62);
    z-index: 2;
    pointer-events: none;
  }

  .contacto-panel-content {
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    gap: 1.35rem;
    width: 100%;
    padding: 1.1rem 1.8rem 2rem;
    transform: none;
  }

  .contacto-kicker {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #ffffff;
    font-weight: 700;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  h1 {
    margin: 0;
    color: #ffffff;
    font-size: 2.5rem;
    line-height: 1.12;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.45);
    margin-top: 60px;
  }

  p {
    margin: 0;
    color: #ffffff;
    line-height: 1.5;
    font-weight: 500;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
  }

  .contacto-illustration {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    z-index: 1;
    opacity: 0.78;
  }
}

.contacto-form {
  background: #fff6ee;
  padding: 2.2rem 1.2rem;
  text-shadow: none;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  margin-bottom: 1.3rem;
}

.campo label {
  color: #5a3f37;
  font-weight: 600;
}

.campo input,
.campo textarea {
  border: 1px solid #e1d2c6;
  background: #fffaf6;
  border-radius: 999px;
  box-shadow: 1px 1px 5px rgba(169, 135, 126, 0.12);
  padding: 0.7rem 0.8rem;
  font: inherit;
  color: #2b1b17;
}

.campo textarea {
  border-radius: 16px;
  resize: none;
}

.campo input:focus,
.campo textarea:focus {
  outline: 2px solid rgba(27, 79, 214, 0.25);
  border-color: #1b4fd6;
}

.acciones {
  margin-top: 0.8rem;
}

.btn-principal {
  border: none;
  border-radius: 999px;
  background: #6d534d;
  color: #fff;
  padding: 0.8rem 1.2rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-principal:disabled {
  background: #b9aaa1;
  cursor: not-allowed;
}

.btn-principal:hover:not(:disabled) {
  background: #4a3530;
}

.feedback {
  margin: 0.9rem 0 0;
  border-radius: 10px;
  padding: 0.7rem 0.85rem;
  font-weight: 600;
}

.feedback.ok {
  background: #ecfdf3;
  color: #05603a;
  border: 1px solid #a6f4c5;
}

.feedback.error {
  background: #fef3f2;
  color: #b42318;
  border: 1px solid #fecdca;
}

@media (max-width: 860px) {
  .contacto-card {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
  }
  .contacto-panel {
    display: none !important;
  }
}
@media (max-width: 600px) {
  .contacto-form {
    padding: 1.1rem 0.7rem;
    max-width: 99vw;
    max-height: 98vh;
    min-height: 520px;
    overflow-y: visible;
  }
  .campo input,
  .campo textarea {
    padding: 0.7rem 0.7rem;
    font-size: 1.08rem;
  }
  .campo textarea {
    min-height: 70px;
    max-height: 180px;
  }
}
</style>
