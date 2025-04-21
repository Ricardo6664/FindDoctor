import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../CSS/index.css'
import Header from './header.jsx'
import Footer from './footer.jsx'
import Filtro from './filtro.jsx'
import Mapa from './mapa.jsx'
import Tabela from './tabela.jsx'

createRoot(document.getElementById('header')).render(
  <StrictMode>
    <Header/>
  </StrictMode>,
)

createRoot(document.getElementById('filtro')).render(
  <StrictMode>
    <Filtro />
  </StrictMode>,
)

createRoot(document.getElementById('mapa')).render(
  <StrictMode>
    <Mapa />
  </StrictMode>,
)

createRoot(document.getElementById('tabela')).render(
  <StrictMode>
    <Tabela />
  </StrictMode>,
)

createRoot(document.getElementById('footer')).render(
  <StrictMode>
    <Footer />
  </StrictMode>,
)
