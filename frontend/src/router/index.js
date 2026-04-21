import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/reservas',
    name: 'reservas',
    component: () => import('../views/HacerReservasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mis-reservas',
    name: 'my-bookings',
    component: () => import('../views/UserReservasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/reservas',
    name: 'admin-bookings',
    component: () => import('../views/AdminReservasView.vue'),
    meta: { requiresAuth: true, role: 'admin' } 
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

// Este código se ejecuta antes de cada cambio de página
router.beforeEach((to, from, next) => {
  // Comprobamos si la ruta a la que va requiere estar logueado
  const rutaProtegida = to.matched.some(record => record.meta.requiresAuth);
  const estaLogueado = localStorage.getItem('user-token');

  if (rutaProtegida && !estaLogueado) {
    // Si es protegida y no hay token, al Login de cabeza
    next('/login');
  } else {
    // Si todo está bien o la ruta es pública, adelante
    next();
  }
});