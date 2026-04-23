<template>
  <div class="reservar-tour-view">
    <div class="tour-wrap">
      <div class="tour-card">
        <aside class="tour-panel">
          <div class="tour-panel-content">
            <p class="tour-kicker">Visitas guiadas CoWorkFlow</p>
            <h1>Reservar Tour</h1>
            <p>
              Completa el formulario para visitar {{ nombreSedeSeleccionada }}.
              Te confirmaremos por correo lo antes posible.
            </p>
          </div>
          <img :src="require('@/assets/cowork-illustration.png')" alt="Visita guiada en coworking" class="tour-illustration" />
        </aside>

        <form class="tour-form" @submit.prevent="enviarFormulario">
          <div class="campo">
            <label for="tour-nombre">Nombre completo</label>
            <input id="tour-nombre" v-model.trim="form.nombreCompleto" type="text" required maxlength="120" />
          </div>

          <div class="campo">
            <label for="tour-correo">Correo</label>
            <input id="tour-correo" v-model.trim="form.correo" type="email" required maxlength="180" />
          </div>

          <div class="campo">
            <label for="tour-telefono">Num. teléfono</label>
            <input id="tour-telefono" v-model.trim="form.telefono" type="tel" required maxlength="30" />
          </div>

          <div class="campo campo-duo">
            <div>
              <label for="tour-fecha">Fecha</label>
              <input id="tour-fecha" v-model="form.fecha" type="date" required />
            </div>
            <div>
              <label for="tour-hora">Hora</label>
              <input id="tour-hora" v-model="form.hora" type="time" required />
            </div>
          </div>

          <div class="campo campo-duo">
            <div>
              <label for="tour-personas">Número de personas</label>
              <input id="tour-personas" v-model.number="form.personas" type="number" min="1" max="40" required />
            </div>
            <div>
              <label for="tour-empresa">Nombre de la empresa/autónomo</label>
              <input id="tour-empresa" v-model.trim="form.empresa" type="text" required maxlength="160" />
            </div>
          </div>

          <div class="acciones">
            <button class="btn-principal" type="submit" :disabled="enviando">
              {{ enviando ? 'Enviando...' : 'Solicitar tour' }}
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
  name: 'ReservarTourView',
  data() {
    return {
      enviando: false,
      form: {
        nombreCompleto: '',
        correo: '',
        telefono: '',
        fecha: '',
        hora: '',
        personas: 1,
        empresa: ''
      },
      sedesDisponibles: {
        ruzafa: 'Crea. Ruzafa',
        'el-carmen': 'Crea. El Carmen',
        eixample: 'Crea. Eixample',
        'el-cabanyal': 'Crea. El Cabanyal'
      },
      estado: {
        tipo: '',
        mensaje: ''
      }
    };
  },
  computed: {
    sedeSlug() {
      return (this.$route?.query?.sede || '').toString().trim().toLowerCase();
    },
    nombreSedeSeleccionada() {
      const sede = this.sedeSlug;
      if (!sede) return 'la sede seleccionada';
      return this.sedesDisponibles[sede] || 'la sede seleccionada';
    }
  },
  created() {
    const user = this.$store?.state?.user;
    if (user?.full_name) this.form.nombreCompleto = user.full_name;
    if (user?.email) this.form.correo = user.email;
  },
  methods: {
    async validarDisponibilidadTour(token) {
      if (!this.sedeSlug) {
        this.estado = {
          tipo: 'error',
          mensaje: 'Selecciona una sede desde el botón de Reservar Tour.'
        };
        return false;
      }

      try {
        const response = await axios.post(
          'http://localhost:8000/api/bookings/tour-availability',
          {
            sede: this.sedeSlug,
            fecha: this.form.fecha,
            hora: this.form.hora
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        return !!response.data?.available;
      } catch (error) {
        if (error?.response?.status === 409) {
          const conflict = error.response.data?.conflict;
          this.estado = {
            tipo: 'error',
            mensaje: conflict
              ? `Ese horario ya está ocupado (${conflict.room_name}: ${conflict.start} - ${conflict.end}).`
              : (error.response.data?.message || 'Ese horario ya está ocupado para la sede seleccionada.')
          };
          return false;
        }

        this.estado = {
          tipo: 'error',
          mensaje: error?.response?.data?.message || 'No se pudo validar la disponibilidad del tour.'
        };
        return false;
      }
    },
    async enviarFormulario() {
      this.estado = { tipo: '', mensaje: '' };
      this.enviando = true;

      try {
        const token = localStorage.getItem('user-token');
        if (!token) {
          this.estado = {
            tipo: 'error',
            mensaje: 'Debes iniciar sesión para reservar un tour.'
          };
          return;
        }

        const disponible = await this.validarDisponibilidadTour(token);
        if (!disponible) return;

        const payload = {
          sede: this.sedeSlug,
          nombre_completo: this.form.nombreCompleto,
          correo: this.form.correo,
          telefono: this.form.telefono,
          fecha: this.form.fecha,
          hora: this.form.hora,
          personas: this.form.personas,
          empresa: this.form.empresa
        };

        const response = await axios.post(
          'http://localhost:8000/api/bookings/tour-reservations',
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.estado = {
          tipo: 'ok',
          mensaje: response.data?.message || 'Tour reservado correctamente.'
        };

        this.form.telefono = '';
        this.form.fecha = '';
        this.form.hora = '';
        this.form.personas = 1;
        this.form.empresa = '';
      } catch (error) {
        this.estado = {
          tipo: 'error',
          mensaje: error?.response?.data?.message || 'No se pudo enviar la solicitud de tour.'
        };
      } finally {
        this.enviando = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.reservar-tour-view {
  min-height: 100vh;
  padding: 7.5rem 1.25rem 2rem;
  background: linear-gradient(180deg, #fbf7f4 0%, #f6f0eb 100%);
}

.tour-wrap {
  max-width: 980px;
  margin: 0 auto;
}

.tour-card {
  display: grid;
  grid-template-columns: minmax(260px, 0.92fr) minmax(340px, 1fr);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #eaddd3;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  text-shadow: none;
}

.tour-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  min-height: 360px;

  .tour-panel-content {
    position: relative;
    z-index: 2;
    padding: 2rem 1.8rem;
  }

  .tour-kicker {
    margin: 0 0 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.78rem;
    color: #f6ece4;
    font-weight: 700;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  h1 {
    margin: 0;
    color: #ffffff;
    font-size: 2rem;
    line-height: 1.12;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.45);
  }

  p {
    margin: 0.75rem 0 0;
    color: #f5ebe4;
    line-height: 1.5;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
  }

  .tour-illustration {
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

.tour-form {
  background: #fff;
  padding: 1.7rem;
  text-shadow: none;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-bottom: 0.85rem;
}

.campo-duo {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;

  > div {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
}

.campo label {
  color: #5a3f37;
  font-weight: 600;
}

.campo input {
  border: 1px solid #e1d2c6;
  border-radius: 999px;
  padding: 0.7rem 0.8rem;
  font: inherit;
  color: #2b1b17;
}

.campo input:focus {
  outline: 2px solid rgba(27, 79, 214, 0.25);
  border-color: #1b4fd6;
}

.acciones {
  margin-top: 0.8rem;
}

.btn-principal {
  border: none;
  border-radius: 999px;
  background: #362521;
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
  .tour-card {
    grid-template-columns: 1fr;
  }

  .tour-panel {
    padding: 1.5rem;
  }

  .tour-form {
    padding: 1.25rem;
  }

  .campo-duo {
    grid-template-columns: 1fr;
  }
}
</style>
