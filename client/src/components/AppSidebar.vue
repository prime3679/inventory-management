<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div class="sidebar-top">
      <div class="sidebar-brand">
        <div class="brand-icon">CC</div>
        <div class="brand-text" v-show="!collapsed">
          <h1>{{ t('nav.companyName') }}</h1>
          <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" :class="{ active: $route.path === '/' }" :title="collapsed ? t('nav.overview') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>
        <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }" :title="collapsed ? t('nav.inventory') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }" :title="collapsed ? t('nav.orders') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14h6"/><path d="M9 18h6"/><path d="M9 10h6"/></svg>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>
        <router-link to="/spending" :class="{ active: $route.path === '/spending' }" :title="collapsed ? t('nav.finance') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>
        <router-link to="/demand" :class="{ active: $route.path === '/demand' }" :title="collapsed ? t('nav.demandForecast') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }" :title="collapsed ? t('nav.reports') : ''">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>
      </nav>
    </div>

    <div class="sidebar-bottom">
      <div v-show="!collapsed" class="sidebar-bottom-content">
        <LanguageSwitcher />
        <div class="sidebar-divider"></div>
      </div>
      <ProfileMenu
        @show-profile-details="$emit('show-profile-details')"
        @show-tasks="$emit('show-tasks')"
      />
      <div class="sidebar-divider"></div>
      <button class="collapse-btn" @click="toggle" :title="collapsed ? 'Expand sidebar' : 'Collapse sidebar'">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" :class="{ flipped: collapsed }"><polyline points="15 18 9 12 15 6"/></svg>
        <span class="nav-label">Collapse</span>
      </button>
    </div>
  </aside>
</template>

<script>
import { useI18n } from '../composables/useI18n'
import LanguageSwitcher from './LanguageSwitcher.vue'
import ProfileMenu from './ProfileMenu.vue'

export default {
  name: 'AppSidebar',
  components: {
    LanguageSwitcher,
    ProfileMenu
  },
  props: {
    collapsed: {
      type: Boolean,
      default: false
    }
  },
  emits: ['show-profile-details', 'show-tasks', 'update:collapsed'],
  setup(props, { emit }) {
    const { t } = useI18n()

    const toggle = () => {
      emit('update:collapsed', !props.collapsed)
    }

    return { t, toggle }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width, 240px);
  height: 100vh;
  background: var(--color-bg-sidebar, #ffffff);
  border-right: 1px solid var(--color-border, #e2e8f0);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: var(--z-sidebar, 50);
  overflow: visible;
  transition: width 0.2s ease;
}

.sidebar.collapsed {
  width: var(--sidebar-width-collapsed, 64px);
}

.sidebar-top {
  padding-top: 1.25rem;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0 1.25rem 1.25rem;
  border-bottom: 1px solid var(--color-border, #e2e8f0);
  overflow: hidden;
}

.collapsed .sidebar-brand {
  justify-content: center;
  padding: 0 0.875rem 1.25rem;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.025em;
  flex-shrink: 0;
}

.brand-text h1 {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--color-text-primary, #0f172a);
  letter-spacing: -0.025em;
  line-height: 1.3;
  white-space: nowrap;
}

.brand-subtitle {
  font-size: 0.6875rem;
  color: var(--color-text-secondary, #64748b);
  font-weight: 400;
  line-height: 1.3;
  white-space: nowrap;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0.75rem;
}

.collapsed .sidebar-nav {
  padding: 0.75rem 0.5rem;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  color: var(--color-text-secondary, #64748b);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: var(--radius-sm, 6px);
  transition: all 0.15s ease;
  overflow: hidden;
  white-space: nowrap;
}

.collapsed .sidebar-nav a {
  justify-content: center;
  padding: 0.5rem;
}

.sidebar-nav a:hover {
  color: var(--color-text-primary, #0f172a);
  background: var(--color-slate-100, #f1f5f9);
}

.sidebar-nav a.active {
  color: var(--color-accent, #2563eb);
  background: var(--color-accent-light, #eff6ff);
  font-weight: 600;
}

.sidebar-nav a svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.nav-label {
  overflow: hidden;
  white-space: nowrap;
  transition: opacity 0.15s ease, width 0.2s ease;
}

.collapsed .nav-label {
  width: 0;
  opacity: 0;
  overflow: hidden;
}

.sidebar-bottom {
  padding: 0.75rem;
  border-top: 1px solid var(--color-border, #e2e8f0);
  position: relative;
  z-index: 10;
}

.collapsed .sidebar-bottom {
  padding: 0.5rem;
}

.sidebar-bottom-content {
  overflow: hidden;
}

.sidebar-divider {
  height: 1px;
  background: var(--color-border, #e2e8f0);
  margin: 0.5rem 0;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm, 6px);
  color: var(--color-text-secondary, #64748b);
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  overflow: hidden;
  white-space: nowrap;
}

.collapsed .collapse-btn {
  justify-content: center;
  padding: 0.5rem;
}

.collapse-btn:hover {
  color: var(--color-text-primary, #0f172a);
  background: var(--color-slate-100, #f1f5f9);
}

.collapse-btn svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.collapse-btn svg.flipped {
  transform: rotate(180deg);
}
</style>
