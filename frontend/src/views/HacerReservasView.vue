<template>
  <div class="contenedor-reservas">
    <div class="tarjeta-reserva">
      <aside class="reserva-panel">
        <p class="reserva-kicker">Reserva inteligente</p>
        <h2>Nueva reserva</h2>
        <p>Configura fecha, tramo horario y confirma tu espacio.</p>
        <img :src="require('@/assets/reserva-salas.png')" alt="Reserva de salas" class="reserva-illustration" />
      </aside>

      <div class="reserva-form-area">
        <p v-if="salaNombre" class="sala-seleccionada">Estás reservando: <strong>{{ salaNombre }}</strong></p>

        <div class="selector-tipo">
          <label>Tipo de reserva</label>
          <div class="opciones-tipo">
            <button
              type="button"
              :class="['opcion-tipo', { activo: tipoReserva === 'horas' }]"
              @click="tipoReserva = 'horas'"
            >
              <span class="icono">⏱️</span>
              <span class="texto">Reserva por Horas</span>
              <span class="subtexto">(Sala)</span>
            </button>
            <button
              type="button"
              :class="['opcion-tipo', { activo: tipoReserva === 'diario' }]"
              @click="tipoReserva = 'diario'"
            >
              <span class="icono">🪑</span>
              <span class="texto">Pase Diario</span>
              <span class="subtexto">(Puesto Flexible)</span>
            </button>
          </div>
        </div>

        <form @submit.prevent="confirmarReserva" class="formulario">
          <!-- RESERVA POR HORAS -->
          <template v-if="tipoReserva === 'horas'">
            <div class="campo" v-if="!salaFijadaPorRuta">
              <label>Sala</label>
              <select v-model="salaId" required>
                <option disabled value="">Selecciona una sala</option>
                <option v-for="sala in salasDisponibles" :key="sala.id" :value="String(sala.id)">
                  {{ sala.name }} · {{ sala.location || 'Sin ubicación' }} · {{ sala.capacity }} personas · {{ sala.price_per_hour }}€/h
                </option>
              </select>
            </div>

            <div class="campo" v-else>
              <label>Sala</label>
              <input
                type="text"
                :value="textoSalaFijada"
                readonly
                disabled
              >
            </div>

            <div class="campo">
              <label>Fecha</label>
              <input v-model="fecha" type="date" :min="hoy" required>
            </div>

            <div class="campo-grupo">
              <div class="campo">
                <label>Hora Inicio</label>
                <input v-model="horaInicio" type="time" required>
              </div>
              <div class="campo">
                <label>Hora Fin</label>
                <input v-model="horaFin" type="time" required>
              </div>
            </div>

            <div class="resumen" v-if="salaSeleccionada && fecha && horaInicio && horaFin">
              <div class="resumen-item">
                <span>Duración</span>
                <strong>{{ duracionHoras.toFixed(2) }} h</strong>
              </div>
              <div class="resumen-item">
                <span>Tarifa</span>
                <strong>{{ Number(salaSeleccionada.price_per_hour || 0).toFixed(2) }} €/h</strong>
              </div>
              <div class="resumen-item total">
                <span>Total estimado</span>
                <strong>{{ totalEstimado.toFixed(2) }} €</strong>
              </div>
            </div>
          </template>

          <!-- PASE DIARIO -->
          <template v-else-if="tipoReserva === 'diario'">
            <div class="campo">
              <label>Fecha del pase</label>
              <input v-model="fechaDiario" type="date" :min="hoy" required>
            </div>

            <div class="campo">
              <label>Cantidad de días</label>
              <select v-model.number="cantidadDias" required>
                <option value="">Selecciona cantidad</option>
                <option value="1">1 día - 35€</option>
                <option value="5">5 días - 160€</option>
                <option value="10">10 días (bono) - 280€</option>
              </select>
            </div>

            <div class="info-diario">
              <p>✨ Acceso flexible a puestos de trabajo en la sede principal</p>
              <p>📍 Ubicación: Valencia Centro</p>
              <p>🕐 Horario: 9:00 - 18:00</p>
            </div>

            <div class="resumen" v-if="fechaDiario && cantidadDias">
              <div class="resumen-item">
                <span>Cantidad</span>
                <strong>{{ cantidadDias }} {{ cantidadDias === 1 ? 'día' : 'días' }}</strong>
              </div>
              <div class="resumen-item">
                <span>Precio por día</span>
                <strong>{{ precioUnitarioDiario.toFixed(2) }} €</strong>
              </div>
              <div class="resumen-item total">
                <span>Total estimado</span>
                <strong>{{ totalDiario.toFixed(2) }} €</strong>
              </div>
            </div>
          </template>

          <div class="metodo-pago">
            <label>Método de pago</label>
            <div class="metodo-pago-opciones">
              <button
                type="button"
                class="metodo-btn deshabilitado"
                disabled
                style="opacity: 0.5; cursor: not-allowed;"
              >
                <span class="titulo">Pagar en la plataforma</span>
                <span class="detalle">Disponible  proximamente</span>
              </button>

              <button
                type="button"
                :class="['metodo-btn', { activo: metodoPago === 'recepcion' }]"
                @click="metodoPago = 'recepcion'"
              >
                <span class="titulo">Pagar en recepción</span>
                <span class="detalle">Reserva guardada con pago pendiente</span>
              </button>
            </div>
          </div>

          <button type="submit" :disabled="cargando || !puedeEnviar" class="boton-reserva">
            {{ textoBotonConfirmar }}
          </button>
        </form>

        <p v-if="mensaje" :class="['mensaje', esError ? 'error' : 'exito']">
          {{ mensaje }}
        </p>
      </div>
    </div>

    <div v-if="mostrarModalPago" class="modal-overlay" @click.self="cerrarModalPago">
      <div class="modal-pago">
        <p class="modal-kicker">Pasarela premium Crea.</p>
        <h3>Finalizar pago seguro</h3>
        <p class="modal-copy">
          Introduce una tarjeta ficticia para simular el pago.
          Puedes usar <strong>4242 4242 4242 4242</strong> como ejemplo.
        </p>

        <div class="campo">
          <label>Número de tarjeta</label>
          <input
            v-model="tarjeta.numero"
            type="text"
            inputmode="numeric"
            placeholder="4242 4242 4242 4242"
            maxlength="23"
            @input="formatearNumeroTarjeta"
          >
        </div>

        <div class="campo">
          <label>Titular</label>
          <input v-model="tarjeta.titular" type="text" placeholder="Nombre del titular">
        </div>

        <div class="campo-grupo">
          <div class="campo">
            <label>Caducidad</label>
            <input v-model="tarjeta.caducidad" type="text" placeholder="MM/AA" maxlength="5">
          </div>
          <div class="campo">
            <label>CVV</label>
            <input v-model="tarjeta.cvv" type="text" inputmode="numeric" placeholder="123" maxlength="4">
          </div>
        </div>

        <p v-if="mensajePago" class="mensaje error">{{ mensajePago }}</p>

        <div class="modal-acciones">
          <button type="button" class="btn-secundario" :disabled="procesandoPago" @click="cerrarModalPago">
            Cancelar
          </button>
          <button type="button" class="btn-principal" :disabled="procesandoPago" @click="procesarPagoSeguro">
            {{ procesandoPago ? 'Procesando pago seguro...' : 'Pagar y confirmar reserva' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ReservasView',
  data() {
    return {
      tipoReserva: 'horas',
      // Reserva por horas
      salaId: this.$route.query.sala ? String(this.$route.query.sala) : '',
      salaNombre: this.$route.query.nombre || '',
      salasDisponibles: [],
      fecha: '',
      horaInicio: '',
      horaFin: '',
      // Pase diario
      fechaDiario: '',
      cantidadDias: '',
      metodoPago: 'recepcion',
      cargando: false,
      procesandoPago: false,
      mostrarModalPago: false,
      reservaPendiente: null,
      mensajePago: '',
      tarjeta: {
        numero: '',
        titular: '',
        caducidad: '',
        cvv: ''
      },
      mensaje: '',
      esError: false,
      hoy: this.fechaLocalHoy()
    }
  },
  computed: {
    salaFijadaPorRuta() {
      return Boolean(this.$route.query.sala);
    },
    salaSeleccionada() {
      return this.salasDisponibles.find(s => String(s.id) === String(this.salaId)) || null;
    },
    textoSalaFijada() {
      if (this.salaSeleccionada) {
        return `${this.salaSeleccionada.name} · ${this.salaSeleccionada.location || 'Sin ubicación'} · ${this.salaSeleccionada.capacity} personas · ${this.salaSeleccionada.price_per_hour}€/h`;
      }
      if (this.salaNombre) return this.salaNombre;
      return 'Sala seleccionada';
    },
    duracionHoras() {
      if (!this.horaInicio || !this.horaFin) return 0;
      const [hi, mi] = this.horaInicio.split(':').map(Number);
      const [hf, mf] = this.horaFin.split(':').map(Number);
      const inicioMin = (hi * 60) + mi;
      const finMin = (hf * 60) + mf;
      if (finMin === inicioMin) return 0;

      let diferencia = finMin - inicioMin;
      if (diferencia < 0) {
        // Permite tramos que pasan a la madrugada (ej: 23:00 -> 02:00)
        diferencia += 24 * 60;
      }

      return diferencia / 60;
    },
    totalEstimado() {
      if (!this.salaSeleccionada) return 0;
      return this.duracionHoras * Number(this.salaSeleccionada.price_per_hour || 0);
    },
    puedeEnviar() {
      if (this.tipoReserva === 'horas') {
        return Boolean(this.salaId && this.fecha && this.horaInicio && this.horaFin && this.duracionHoras > 0);
      } else if (this.tipoReserva === 'diario') {
        return Boolean(this.fechaDiario && this.cantidadDias);
      }
      return false;
    },
    precioUnitarioDiario() {
      const precios = {
        1: 35,
        5: 32,
        10: 28
      };
      return precios[this.cantidadDias] || 0;
    },
    totalDiario() {
      return this.cantidadDias * this.precioUnitarioDiario;
    },
    textoBotonConfirmar() {
      if (this.cargando) return 'Procesando...';
      if (this.metodoPago === 'plataforma') return 'Ir a pago seguro';
      return 'Confirmar Reserva';
    }
  },
  async created() {
    await this.obtenerSalas();

    if (this.salaId && !this.salaNombre) {
      const sala = this.salasDisponibles.find(s => String(s.id) === String(this.salaId));
      if (sala) this.salaNombre = sala.name;
    }
  },
  methods: {
    fechaLocalHoy() {
      const d = new Date();
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    },
    async obtenerSalas() {
      try {
        const response = await axios.get('http://localhost:8000/api/rooms/');
        this.salasDisponibles = (response.data || []).filter(sala => sala.is_active);
      } catch (error) {
        console.error('Error al cargar salas:', error);
      }
    },
    construirPayloadReservaHoras() {
      if (!this.salaId) throw new Error('Debes seleccionar una sala.');
      if (!this.fecha) throw new Error('Debes seleccionar una fecha.');
      if (this.duracionHoras <= 0) throw new Error('La franja horaria no es válida.');

      const [hi, mi] = this.horaInicio.split(':').map(Number);
      const [hf, mf] = this.horaFin.split(':').map(Number);
      const inicioMin = (hi * 60) + mi;
      const finMin = (hf * 60) + mf;

      const inicioDate = new Date(`${this.fecha}T${this.horaInicio}:00`);
      const finDate = new Date(`${this.fecha}T${this.horaFin}:00`);

      if (finMin < inicioMin) {
        finDate.setDate(finDate.getDate() + 1);
      }

      const toDateTimeString = (dateObj) => {
        const y = dateObj.getFullYear();
        const m = String(dateObj.getMonth() + 1).padStart(2, '0');
        const d = String(dateObj.getDate()).padStart(2, '0');
        const h = String(dateObj.getHours()).padStart(2, '0');
        const min = String(dateObj.getMinutes()).padStart(2, '0');
        return `${y}-${m}-${d} ${h}:${min}:00`;
      };

      return {
        room_id: Number(this.salaId),
        start_time: toDateTimeString(inicioDate),
        end_time: toDateTimeString(finDate)
      };
    },
    async guardarReservaHoras(payload, paymentStatus, paymentMethod) {
      const token = localStorage.getItem('user-token');
      if (!token) throw new Error('Debes iniciar sesión para reservar.');

      await axios.post(
        'http://localhost:8000/api/bookings/',
        {
          ...payload,
          payment_status: paymentStatus,
          payment_method: paymentMethod
        },
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
    },
    guardarPaseDiario(paymentStatus, paymentMethod) {
      const pasesDiarios = JSON.parse(localStorage.getItem('pases-diarios') || '[]');
      pasesDiarios.push({
        id: Date.now(),
        tipo: 'pase-diario',
        fechaInicio: this.fechaDiario,
        cantidadDias: this.cantidadDias,
        total: this.totalDiario,
        payment_status: paymentStatus,
        payment_method: paymentMethod,
        creado: new Date().toISOString()
      });
      localStorage.setItem('pases-diarios', JSON.stringify(pasesDiarios));
    },
    formatearNumeroTarjeta() {
      const soloDigitos = this.tarjeta.numero.replace(/\D/g, '').slice(0, 19);
      this.tarjeta.numero = soloDigitos.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
    },
    abrirModalPago(reservaPendiente) {
      this.reservaPendiente = reservaPendiente;
      this.mensajePago = '';
      this.mostrarModalPago = true;
    },
    cerrarModalPago() {
      if (this.procesandoPago) return;
      this.mostrarModalPago = false;
      this.mensajePago = '';
    },
    validarTarjetaFicticia() {
      const numero = this.tarjeta.numero.replace(/\s/g, '');
      const esNumeroValido = /^\d{13,19}$/.test(numero);
      const esTitularValido = Boolean(this.tarjeta.titular.trim());
      const esCaducidadValida = /^(0[1-9]|1[0-2])\/(\d{2})$/.test(this.tarjeta.caducidad);
      const esCvvValido = /^\d{3,4}$/.test(this.tarjeta.cvv);

      if (!esNumeroValido || !esTitularValido || !esCaducidadValida || !esCvvValido) {
        this.mensajePago = 'Datos inválidos. Usa 13-19 dígitos, titular, caducidad MM/AA (01-12) y CVV de 3-4 dígitos.';
        return false;
      }

      return true;
    },
    async procesarPagoSeguro() {
      if (!this.reservaPendiente) {
        this.mensajePago = 'No hay una reserva pendiente de pago.';
        return;
      }

      if (!this.validarTarjetaFicticia()) return;

      this.procesandoPago = true;
      this.mensajePago = '';

      try {
        await new Promise(resolve => setTimeout(resolve, 1400));

        if (this.reservaPendiente.tipo === 'horas') {
          await this.guardarReservaHoras(this.reservaPendiente.payload, 'paid', 'platform');
        } else {
          this.guardarPaseDiario('paid', 'platform');
        }

        this.mostrarModalPago = false;
        this.esError = false;
        this.mensaje = '¡Pago aprobado y reserva confirmada!';
        setTimeout(() => this.$router.push('/mis-reservas'), 1700);
      } catch (err) {
        this.mensajePago = err.response?.data?.message || err.message || 'No se pudo procesar el pago.';
      } finally {
        this.procesandoPago = false;
      }
    },
    async confirmarReserva() {
      this.mensaje = '';
      this.esError = false;

      if (this.tipoReserva === 'horas') {
        let payload;
        try {
          payload = this.construirPayloadReservaHoras();
        } catch (err) {
          this.esError = true;
          this.mensaje = err.message;
          return;
        }

        if (this.metodoPago === 'plataforma') {
          this.abrirModalPago({ tipo: 'horas', payload });
          return;
        }

        this.cargando = true;
        try {
          await this.guardarReservaHoras(payload, 'pending', 'reception');
          this.mensaje = 'Reserva guardada. Pago pendiente en recepción.';
          setTimeout(() => this.$router.push('/mis-reservas'), 2000);
        } catch (err) {
          this.esError = true;
          this.mensaje = err.response?.data?.message || err.message || 'Error al realizar la reserva';
        } finally {
          this.cargando = false;
        }
        return;
      }

      if (this.tipoReserva === 'diario') {
        if (this.metodoPago === 'plataforma') {
          this.abrirModalPago({ tipo: 'diario' });
          return;
        }

        this.cargando = true;
        try {
          this.guardarPaseDiario('pending', 'reception');
          this.mensaje = 'Pase guardado. Pago pendiente en recepción.';
          setTimeout(() => this.$router.push('/mis-reservas'), 2000);
        } catch (err) {
          this.esError = true;
          this.mensaje = err.message || 'Error al guardar el pase diario';
        } finally {
          this.cargando = false;
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.contenedor-reservas {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: 2rem 1.25rem;
}

.tarjeta-reserva {
  display: grid;
  grid-template-columns: minmax(260px, 0.9fr) minmax(380px, 1.1fr);
  background: #ffffff;
  border: 1px solid #eaddd3;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 46px rgba(43, 27, 23, 0.12);
  width: 100%;
  max-width: 1080px;
}

.reserva-panel {
  background: linear-gradient(180deg, #f4ebe3 0%, #e9ded4 100%);
  position: relative;
  overflow: hidden;
  padding: 2rem 1.8rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.reserva-kicker {
  position: relative;
  z-index: 2;
  margin: 0 0 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.78rem;
  color: #6e5e58;
  font-weight: 700;
}

.reserva-panel h2 {
  position: relative;
  z-index: 2;
  margin: 0;
  font-size: 2rem;
  color: #2b1b17;
  line-height: 1.12;
}

.reserva-panel p {
  position: relative;
  z-index: 2;
  margin: 0.75rem 0 0;
  color: #5a463f;
  line-height: 1.5;
}

.reserva-illustration {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: 1;
  opacity: 0.22;
}

.reserva-form-area {
  padding: 1.75rem;
}

.tarjeta-reserva,
.tarjeta-reserva * {
  text-shadow: none !important;
}

.selector-tipo {
  margin-bottom: 1.5rem;

  label {
    display: block;
    margin-bottom: 0.6rem;
    font-weight: 600;
    color: #2b1b17;
  }
}

.opciones-tipo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
}

.opcion-tipo {
  padding: 1rem;
  border: 2px solid #e2d7cf;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;

  &:hover {
    border-color: #1b4fd6;
    background: #f8f3ef;
  }

  &.activo {
    border-color: #1b4fd6;
    background: #eef5ff;
  }

  .icono {
    font-size: 1.5rem;
  }

  .texto {
    font-weight: 600;
    color: #2b1b17;
    font-size: 0.9rem;
  }

  .subtexto {
    font-size: 0.75rem;
    color: #8c7e7a;
  }
}

.info-diario {
  background: #fcfaf7;
  border: 1px solid #eaddd3;
  border-radius: 8px;
  padding: 1rem;
  margin: 0.5rem 0 1.2rem;

  p {
    margin: 0.35rem 0;
    color: #5a3f37;
    font-size: 0.9rem;
  }
}

h2 {
  margin: 0;
  font-size: 2rem;
  color: #2b1b17;
}

.intro {
  margin: 0.35rem 0 1.2rem;
  color: #8c7e7a;
}

.sala-seleccionada {
  background: #f6efe9;
  border: 1px solid #eaddd3;
  padding: 0.7rem 0.9rem;
  border-radius: 8px;
  color: #5a3f37;
  margin-bottom: 1.5rem;
}

.campo-grupo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.campo {
  margin-bottom: 1.2rem;
  label { display: block; margin-bottom: 0.45rem; font-weight: 600; text-align: left; color: #2b1b17; }
  input, select {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #e2d7cf;
    border-radius: 999px;
    font-family: inherit;
    font-size: 1rem;
    color: #2b1b17;
    background: #fff;
    outline: none;
  }

  input[type='date'],
  input[type='time'] {
    border-radius: 14px;
  }

  select {
    border-radius: 14px;
  }

  input:focus, select:focus {
    border-color: #1b4fd6;
    box-shadow: 0 0 0 3px rgba(27, 79, 214, 0.14);
  }
}

.resumen {
  border: 1px solid #eaddd3;
  background: #fcfaf7;
  border-radius: 8px;
  padding: 0.9rem;
  margin: 0.5rem 0 1.2rem;
}

.resumen-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #6e5e58;
  font-size: 0.92rem;
}

.resumen-item + .resumen-item {
  margin-top: 0.45rem;
}

.resumen-item strong {
  color: #2b1b17;
}

.resumen-item.total {
  margin-top: 0.65rem;
  padding-top: 0.65rem;
  border-top: 1px solid #eadfd8;
}

.boton-reserva {
  width: 100%;
  padding: 0.95rem;
  background-color: #362521;
  color: white;
  border: none;
  border-radius: 999px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  &:hover { background-color: #4a3530; }
  &:disabled { background-color: #b9aaa1; cursor: not-allowed; }
}

.metodo-pago {
  margin: 0.2rem 0 1.2rem;

  > label {
    display: block;
    margin-bottom: 0.55rem;
    font-weight: 600;
    color: #2b1b17;
    text-align: left;
  }
}

.metodo-pago-opciones {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
}

.metodo-btn {
  border: 1px solid #dfd2c7;
  background: #fffcf8;
  border-radius: 14px;
  padding: 0.75rem;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;

  .titulo {
    display: block;
    color: #2e201b;
    font-weight: 700;
    font-size: 0.9rem;
  }

  .detalle {
    display: block;
    margin-top: 0.2rem;
    color: #7b655a;
    font-size: 0.78rem;
    line-height: 1.25;
  }

  &:hover {
    border-color: #bcaea3;
  }

  &.activo {
    border-color: #5d4035;
    background: #f5ece4;
    box-shadow: inset 0 0 0 1px rgba(93, 64, 53, 0.18);
  }
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(20, 12, 9, 0.54);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 1200;
}

.modal-pago {
  width: min(520px, 100%);
  background: linear-gradient(180deg, #fffaf5 0%, #f6ede5 100%);
  border: 1px solid #ddcec2;
  border-radius: 18px;
  padding: 1.25rem;
  box-shadow: 0 24px 60px rgba(43, 27, 23, 0.34);
}

.modal-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  color: #7f675b;
  font-weight: 700;
}

.modal-pago h3 {
  margin: 0.3rem 0 0.45rem;
  color: #2b1b17;
}

.modal-copy {
  margin: 0 0 1rem;
  color: #5d4a42;
  font-size: 0.92rem;
  line-height: 1.45;
}

.modal-acciones {
  margin-top: 0.9rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
}

.btn-secundario,
.btn-principal {
  border: none;
  border-radius: 999px;
  padding: 0.68rem 1rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-secundario {
  background: #efe3d7;
  color: #4a352d;
}

.btn-principal {
  background: #3a2923;
  color: #ffffff;
}

.btn-secundario:disabled,
.btn-principal:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.mensaje {
  margin-top: 1rem;
  padding: 0.65rem 0.8rem;
  border-radius: 8px;
  &.exito { background: #eaf7ed; color: #1b7a3d; border: 1px solid #caecd3; }
  &.error { background: #fdecec; color: #b42318; border: 1px solid #f8d0d0; }
}

@media (max-width: 640px) {
  .tarjeta-reserva {
    grid-template-columns: 1fr;
  }

  .reserva-panel {
    padding: 1.4rem;
  }

  .reserva-form-area {
    padding: 1.2rem;
  }

  .campo-grupo {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .metodo-pago-opciones {
    grid-template-columns: 1fr;
  }

  .modal-acciones {
    flex-direction: column;
  }
}
</style>