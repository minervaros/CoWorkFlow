import { createStore } from 'vuex'

export default createStore({
  state: {
    // Aquí definimos las variables globales
    token: localStorage.getItem('user-token') || '',
    user: null
  },
  getters: {
    // Para saber de forma rápida si el usuario está logueado
    isLoggedIn: state => !!state.token,
    getUser: state => state.user
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
    },
    SET_USER(state, user) {
      state.user = user;
    },
    LOGOUT(state) {
      state.token = '';
      state.user = null;
    }
  },
  actions: {
    saveLogin({ commit }, { token, user }) {
      localStorage.setItem('user-token', token); // Lo guardamos en el navegador
      commit('SET_TOKEN', token);
      commit('SET_USER', user);
    },
    logout({ commit }) {
      localStorage.removeItem('user-token');
      commit('LOGOUT');
    }
  },
  modules: {
  }
})
