import { createStore } from 'vuex'

export default createStore({
  state: {
    token: localStorage.getItem('user-token') || '',
    user: null,
    // Añadimos el rol al estado para que Vuex también lo sepa
    role: localStorage.getItem('user-role') || ''
  },
  getters: {
    isLoggedIn: state => !!state.token,
    getUser: state => state.user,
    getRole: state => state.role
  },
  mutations: {
    // IMPORTANTE: Los nombres aquí deben coincidir con los de las acciones
    SET_TOKEN(state, token) {
      state.token = token;
    },
    SET_USER(state, user) {
      state.user = user;
    },
    SET_ROLE(state, role) {
      state.role = role;
    },
    LOGOUT(state) {
      state.token = '';
      state.user = null;
      state.role = '';
    }
  },
  actions: {
    // Usamos 'payload' para que sea más claro y evitar errores de no-unused-vars
    saveLogin({ commit }, payload) {
      // 1. Guardamos en Vuex usando los nombres de las MUTATIONS
      commit('SET_TOKEN', payload.token);
      commit('SET_USER', payload.user);
      commit('SET_ROLE', payload.user.role);

      // 2. Guardamos en LocalStorage para persistencia
      localStorage.setItem('user-token', payload.token);
      localStorage.setItem('user-role', payload.user.role);
    },
    logout({ commit }) {
      // Limpiamos todo al salir
      localStorage.removeItem('user-token');
      localStorage.removeItem('user-role');
      commit('LOGOUT');
    }
  }
})