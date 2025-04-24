import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue' // Import Register page
import DashboardView from '../views/DashboardView.vue'
import TaskView from '../views/TaskView.vue'

const routes = [
  { path: '/login', component: LoginView, meta: { requiresAuth: false } },
  { path: '/register', component: RegisterView, meta: { requiresAuth: false } }, // Register route
  { path: '/dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/tasks', component: TaskView, meta: { requiresAuth: true } },
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global route guard to prevent access to login/register if logged in
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token'); // Check if the user is authenticated
  if (to.meta.requiresAuth && !isAuthenticated) {
    // If the page requires authentication and the user is not authenticated, redirect to login
    next('/login');
  } else if (!to.meta.requiresAuth && isAuthenticated) {
    // If the page doesn't require authentication and the user is logged in, redirect to dashboard
    next('/dashboard');
  } else {
    next(); // Otherwise, allow access to the page
  }
});

export default router;
