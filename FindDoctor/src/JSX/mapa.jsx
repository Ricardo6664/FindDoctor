import '../CSS/mapa.css'

function Mapa() {
  return (
    <>
      <div className="mapa_container">
        <div className="mapa_content">
            <iframe className="mapa_localizacao" 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7175.925708952284!2d-49.96302752734856!3d-22.236353920628613!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94bfd7653ca18ae3%3A0x6de5ac9f185422f1!2sHospital%20Beneficente%20UNIMAR!5e0!3m2!1spt-BR!2sbr!4v1745266033772!5m2!1spt-BR!2sbr" width="1106" height="600"></iframe>
        </div>
      </div>
    </>
  )
}

export default Mapa
