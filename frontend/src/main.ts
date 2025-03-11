import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// PrimeVue
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import ProgressSpinner from 'primevue/progressspinner'
import Dropdown from 'primevue/dropdown'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Card from 'primevue/card'
import Textarea from 'primevue/textarea'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'

// PrimeVue CSS - Thứ tự rất quan trọng: theme -> core -> icons -> primeflex
import 'primevue/resources/themes/lara-light-indigo/theme.css'  // Theme
import 'primevue/resources/primevue.min.css'                    // Core CSS của PrimeVue
import 'primeicons/primeicons.css'                              // Icons
import 'primeflex/primeflex.css'                                // Flexbox và grid utilities

// Import CSS custom của ứng dụng sau các thư viện
import './assets/main.scss'

const app = createApp(App)

// Sử dụng PrimeVue
app.use(PrimeVue, {
  ripple: true,
  inputStyle: 'filled'
})
app.use(ToastService)
app.use(router)

// Đăng ký các component PrimeVue
app.component('Button', Button)
app.component('InputText', InputText)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('ProgressSpinner', ProgressSpinner)
app.component('Dropdown', Dropdown)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Card', Card)
app.component('Textarea', Textarea)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)

app.mount('#app')